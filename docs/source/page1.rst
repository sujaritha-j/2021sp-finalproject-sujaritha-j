.. _intro:

Project Introduction
=====================

Final Project: Enhanced Product Search (CSCI E-29 - Spring 2021)

Submitted by: Sujaritha Jagadeesan

.. _demo:

Try Enhanced Product Search Demo link
--------------------------------------

Click the below link to test the 'Enhanced Product Search'

`<https://finalproject-spring-2021.s3.amazonaws.com/index.html?>`_

.. _background:

Background and Motivation
--------------------------

In our day-to-day life, we search for products online all the time.Especially during these COVID times,
we rely on online shopping and searching a lot more.
When we shop online, we search for products in retailer's websites.

Typically, many retailer websites use 'search' based on keywords and tagging.
But there are some serious drawbacks to 'keywords' based search.
The first and foremost, it fails to retrieve related products, if the 'search text' doesn't exactly match the keywords
tagged for that product.

For example, when we enter a single word in the 'search box', the search would return all the relevant products.
But, when we enter more than one word in the search box, the 'search' may not retrieve all the products as expected.
This is simply because the 'search text' did not match the exact keywords that were tagged for the products.

As an alternate to the above drawback, I wanted to leverage 'Word Embedding' and 'word2vec' to search and retrieve
products that are more aligned with the customer search text.
So for the final project, I explored and implemented 'Enhanced product search' based on 'Word Embedding' and 'word2vec'.

.. _goal:

Project Goal
------------

To propose and demonstrate an 'Enhanced product search', built on python, leveraging 'Word Embedding' and 'word2vec'.
By vectorizing the product description and the search text, we find the cosine similarity and the distance between them
to return the top matching products.
This would help in better understanding the consumer's search intent and matching with products close to consumers need.


