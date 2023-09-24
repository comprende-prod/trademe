# Ideas for extending `trademe`:
Some ways you could improve the package:
## Larger searches:
If we start doing larger searches (e.g. returning thousands/tens of thousands of results), it's probably a good idea to:
- Search: add options for more concurrency in individual calls of `search()`. For example, you could write some kind of wrapper that distributes an arbitrary number of threads between some number of searches. Currently, the program leaves it up to you to do this.
- Storage: thousands/tens of thousands of Listing classes are going to consume a lot of memory. Writing a file manager (like those in many other scraping projects) to efficiently write listing data to a CSV is probably a good idea for really big searches.
## Data validation:
Currently, `make_url()` and `search()` use virtually no data validation. Raising some helpful exceptions/adding some asserts at the start of each method could be useful.
