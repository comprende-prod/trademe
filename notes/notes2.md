# To-dos:
- Update the make_url methods: it needs to support just having one or two (not necessarily all three) location paramters (e.g. if you just want to specify region="wellington", that should be okay). Also make both into one method.
DONE!!!
- Write docstring for make_url - add example kwargs too. (Probs list all of them).
DONE
- Write how-to.ipynb - needs BOTH single-threaded and multi-threaded examples.
DONE
- Also include how someone might make their results into CSV and DataFrame
DONE
- Fix the test stuff - you have a comment in test_search.py for that.
- Write a bunch of tests - we want high coverage! Everything! this includes testing that the right exceptions get raised, etc.
- it also, uh, doesn't do parking anymore. good god. Ask Awhina how essential this is (given you'll need to prioritise pretty seriously).
- Add a stop_page parameter to your search method - should be easy.
- Set up linting or sth? Or just don't.