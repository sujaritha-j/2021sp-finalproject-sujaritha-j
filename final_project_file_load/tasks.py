import dask
import dask.dataframe as dd
import luigi
import pandas as pd
from luigi import Parameter
from luigi.contrib.s3 import S3Target

from word_embedding.embedding import WordEmbedding


class DataDownloadTask(luigi.ExternalTask):
    s3_data_path = Parameter()  # Filename of the image under the root s3 path
    s3_output_path = Parameter()
    columns = ['uniq_id', 'product_name', 'brand_name', 'p_asin', 'category', 'upc_ean_code', 'list_price',
               'selling_price', 'quantity', 'model_number, about_product', 'product_specification',
               'technical_details', 'shipping_weight', 'product_dimensions', 'image', 'variants', 'sku',
               'product_url', 'stock', 'product_details, dimensions', 'color', 'ingredients', 'directions_to_use',
               'is_amazon_seller', 'size_quantity_variant', 'product_description']

    def requires(self):
        pass  # pragma: no_cover

    def output(self):
        return S3Target(self.s3_output_path)

    def run(self):
        try:
            # Read from S3
            ddf = dd.read_csv(  # pragma: no_cover
                self.s3_data_path,
                dtype={'Upc Ean Code': 'str'},
                storage_options={
                    'anon': False,
                    'requester_pays': True
                }
            )
            # calculate vector
            cols = ['Uniq Id', 'Product Name', 'Selling Price', 'Image', 'About Product']
            word_embedding = WordEmbedding.from_files('words.txt', 'vectors.npy.gz')
            df_to_write = pd.DataFrame()
            for i in range(ddf.npartitions):
                df_partition = ddf.get_partition(i)[cols].compute()
                product = []
                for index, row in df_partition.iterrows():
                    unique_id = row['Uniq Id']
                    description = row['Product Name']
                    if description is not None:
                        print(unique_id, description)
                        description_vector = word_embedding.embed_document(description)
                        product.append(description_vector)
                df_partition['vectorized_value'] = product
                df_to_write = df_to_write.append(df_partition, ignore_index=True)
            print('Ready to write')
            ddf_to_write = dd.from_pandas(df_to_write, npartitions=ddf.npartitions)
            ddf_to_write.fillna(0)
            file_path = self.output().path + 'product-data-*.csv'
            dask.dataframe.to_csv(df=ddf_to_write, filename=file_path, single_file=False, encoding='utf-8',
                                  mode='wt', name_function=None,
                                  compression=None,
                                  compute=True)
            print('File write complete')
        except Exception as err:
            print('Error: ', err)
