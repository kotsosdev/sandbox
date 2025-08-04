import matplotlib.pyplot as plt
from datetime import datetime
from utils import log, json_load

def prepare(data):
    products = []
    for url, info in data.items():
        product = {
            "url": "",
            "name": "",
            "prices": [],
            "sales": [],
            "timestamps": []
        }

        product["url"] = url
        product["name"] = info["name"]

        for snapshot in info["snapshots"]:
            price = snapshot["price"]
            sale = snapshot["sale"]
            if price is not None and sale is not None:
                product["prices"].append(price)
                product["sales"].append(sale)
            
                timestamp = datetime.strptime(snapshot["timestamp"], "%Y-%m-%d %H:%M:%S")
                product["timestamps"].append(timestamp)

        products.append(product)

        return products

def graph(product):
    plt.plot(product["timestamps"], product["prices"])
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.title("Price over time")
    plt.show()

def main():
    data = json_load()
    products = prepare(data)

    graph(products[0])

if __name__ == "__main__":
    main()