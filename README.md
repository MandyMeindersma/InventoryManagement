Hello! Welcome to my side project to get better at databases and API's

## Flask
I chose to use flask for ease of testing functions. In hindsight I would not have used flask for this take home. Given the fact that you wanted to pass in variables to the function rather than in a request it was a slight headache. I also return helpful logging messages in the request but don't print anything, so if you run it normally you won't see them.

If you would like to run the flask app:
* `pip3 install requirements.txt`
* `export FLASK_APP=run.py`
* `flask run`

Example request flow:</br>
* `http://127.0.0.1:5000/init_catalog` (will default to example input given in problem) </br>
* `http://127.0.0.1:5000/process_restock` (will default to example input given in problem) </br>
* `http://127.0.0.1:5000/process_order`(will default to example input created by me) </br>
* `http://127.0.0.1:5000/process_order/{"order_id":123,"requested":[{"product_id":0,"quantity":1},{"product_id":11,"quantity":2}]}` </br>
* `http://127.0.0.1:5000/process_restock/[{"product_id":0,"quantity":30},{"product_id":1,"quantity":25},{"product_id":2,"quantity":25},{"product_id":3,"quantity":12},{"product_id":4,"quantity":15},{"product_id":5,"quantity":10},{"product_id":6,"quantity":8},{"product_id":7,"quantity":8},{"product_id":8,"quantity":20},{"product_id":9,"quantity":10},{"product_id":10,"quantity":5},{"product_id":11,"quantity":5},{"product_id":12,"quantity":5}]` </br>

## Assumptions/Notes
 * I saved the entire database in a global dictionary.
 * `product_name` wasn't being used anywhere so I decided not to store it. It makes storing the data much less complicated (having a dictionary with a list(size=2) for values rather than having a dictionary with a list(size=3) as values)
     * If I had more time I would have created enums or something for indexing the list so it would be less confusing</br>
 * I attempted to follow PEP8 style guidlines
 * I assume the input into `process_order()` will not give me any `product_id`'s that do not already exsist after `init_catalog()`. This way I do not need to include any error handling in `process_order()`
 * If the full quantity of the order isn't available there are two options:
   * **One:** We send them what we can
   * **Two:** We send them the full order when we restock
   * I am not a doctor so I do not really know the full pros and cons of both options. Is it better for a patient to have half the blood they need? or is it useless at that point and we should just wait until we restock but then by the time we restock will that be too late?
   * I coded option 2


## Known Bugs/Ideal things to refactor (if I had time)
* The recursive function in `packer.py`tries to find the combination of weight containers that will give you the most amount of weight able to transport while minimizing the empty space in the shipment. However, this function assumes that you can use an unlimited ammount of one container (even though someone may have only ordered a set amount). This could be fixed by refactoring the list of containers that is passed into the packer functions. (and therefore some refactoring of `create_shipment`)
* I started to get lazy with some of the variables. Instead of making a dictionary with key value pairs I just made tuples and I remembered what was in each number feild. My naming also got a lot lazier as the challenge went on.
* `create_shipment` kind of became this monster function and I would have liked to break it out into smaller pieces
* There is no input validation


## Feedback given to me from a friend:
* Try to have a packing algorithm that actually works and doesn't need to be refactored and fits the assignment better. Have better rational from why you chose that algorithm. Have a more efficient sollution.
* Know databases and relational databases better
* Didn't meet the tech bar
* Loved my questions and passion
* Do time logging better, like have a better functioning app. How would actual logging in prod look? How would you keep track of inventory better?
