from flask import Flask
from flask import request
from exampleData import *
from packer import Packer
import copy
import json

app = Flask(__name__)

inventory = {}
MAX_WEIGHT = 1800 #1.8kgs
unfulfilled_orders = []

@app.route("/", methods=["GET"])
def hello_world():
    return "Hello World"


@app.route("/init_catalog", defaults={"product_info": product_info_json}, methods=["POST"])
@app.route("/init_catalog/<product_info>", methods=["POST"])
def init_catalog(product_info):
    """
    Initialize inventory in the system. Updates global variable: inventory.
    """
    product_info_loaded = json.loads(product_info)
    quantity = 0
    for product_input in product_info_loaded:
        inventory[product_input["product_id"]] = [product_input["mass_g"], quantity]
    return "Init completed"


@app.route("/process_restock", defaults={"restock": restock_json}, methods=["POST"])
@app.route("/process_restock/<restock>", methods=["POST"])
def process_restock(restock):
    """
    Adds new inventory to the system. Updates global variable: inventory.
    """
    restock_loaded = json.loads(restock)
    for restock_input in restock_loaded:
        inventory[restock_input["product_id"]][1] += restock_input["quantity"]
    for order in unfulfilled_orders:
        process_order(json.dumps(order))
    return "Restock completed"


@app.route("/process_order", defaults={"order": big_order_json}, methods=["POST"])
@app.route("/process_order/<order>", methods=["POST"])
def process_order(order):
    """
    Injects a new order into the system. Calls ship_package if we can make a successful shipment.
    Updates global variable: inventory.
    """
    order_loaded = json.loads(order)
    order_id = order_loaded["order_id"]
    order_details = order_loaded["requested"]

    if is_quantity_available(order_details) == False:
        unfulfilled_orders.append(order_loaded)
        return "Unable to complete order because we do not have enough in stock. We have kept record of your order and on our next restock we will check if we can send it to you then"

    weights_object = parse_weights(order_details)
    shipment_objects = create_shipment(weights_object)

    #adjust inventory
    for shipment in shipment_objects:
        for item in shipment:
            inventory[item["product_id"]][1] -= item["quantity"]
        shipment_dict = {}
        shipment_dict["order_id"] = order_id
        shipment_dict["shipped"] = shipment
        shipment_json = json.dumps(shipment_dict)
        ship_package(shipment_json)
    return "Processed Order"


def ship_package(shipment):
    """
    ships a valid shipment (<1.8kg) and actually have stock to ship.
    We can ship partically filled orders.
    """
    print("\n\nshipment:\n", shipment)
    print("\n\ninventory left:\n", inventory)

#######################################################################################

def is_quantity_available(order_details):
    """
    Goes through inventory to make sure we have the supplies to ship
    """
    quantity_available = True
    for order_input in order_details:
        quantity_available &= (inventory[order_input["product_id"]][1] >= order_input["quantity"])
    return quantity_available

def parse_weights(order_details):
    """
    Instead of having an object with just id's and quantity I want weight to be in the object as well
    """
    weights_object = []
    for item in order_details:
        weight = inventory[item["product_id"]][0]
        product_id = item["product_id"]
        quantity = item["quantity"]
        object = (product_id, weight, quantity)
        weights_object.append(object)
    return weights_object

def parse_shipment(shipment_object):
    """
    Given a shipment array I am turning it into something that resemles the object wanted in the take home
    """
    shipments = []
    for shipment in shipment_object:
        shipment_list = []
        product_id_done = []
        for item in shipment:
            if item not in product_id_done:
                product_id_done.append(item)
                shipment_dict = {}
                shipment_dict["product_id"] = item
                shipment_dict["quantity"] = shipment.count(item)
                shipment_list.append(shipment_dict)
        shipments.append(shipment_list)
    return shipments

def create_shipment(weights_object):
    """
    Calls the recursive function to figure out the most efficient packing.
    Then creates a shipping object to be shipped
    """
    weights = [i[1] for i in weights_object]
    weights_original = copy.copy(weights)
    quantities = [i[2] for i in weights_object if i[2]>0]
    shipment_object = []
    packer = Packer()

    while sum(quantities) > 0:
        packed_tuple = packer.find_most_efficient_packing(MAX_WEIGHT, weights)
        if packed_tuple[1] == []:
            # if there is no possible weight distribution found then just return unsuccessfully
            return []

        shipment = []
        for container_chosen in packed_tuple[1]:
            if weights_object == []:
                #if we have no more containers to ship
                shipment.append(object[0])
                break
            index = weights_original.index(container_chosen)
            object = weights_object[index]

            if object[2] > 0:
                # only if there is quantity left
                shipment.append(object[0])

            weights_object[index] = (object[0], object[1], object[2]-1)
        quantities = [i[2] for i in weights_object]
        weights = [i[1] for i in weights_object if i[2]>0]
        shipment_object.append(shipment)

    shipments = parse_shipment(shipment_object)
    return shipments
