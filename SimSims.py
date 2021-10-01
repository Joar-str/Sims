import random


class Road:

    def __init__(self):
        self._deque = []

    def __len__(self):
        return len(self._deque)

    def has_worker(self):
        return len(self._deque) >= 0

    """FIFO - Först in först ut"""

    def worker_out(self):
        return self._deque.pop(0)

    def worker_in(self, worker):
        self._deque.append(worker)
        if worker.current_life == 0:
            self._deque.remove(worker)

    def get_list(self):
        return self._deque

    def lower_life(self):
        """Om en arbetare har väntat för länge sänks livskraften"""
        pass


class DinningHall:
    """Klassen ska ta in en arbetare från Road() och en enhet mat från Barn()"""

    def __init__(self):

        self._worker_in = None
        self._worker_out = None
        self._food_in = None

    def set_worker_in(self, road):
        self._worker_in = road

    def set_worker_out(self, road):
        self._worker_out = road

    def food_in(self, barn):
        self._food_in = barn

    """Simulergin av intag av mat och arbetare"""

    def simulation_step(self):

        """Tar in en arbetare och en enhet mat från Road1 och barn1 om antalet arbetare är över 2"""

        if self._worker_in.has_worker() and len(self._food_in.inventory) > 0:
            eating_worker = self._worker_in.worker_out()
            food = self._food_in.barn_food_out()
            print(f'arbetare med: {eating_worker} i livskraft går från \n '
                  f'Road1 till matsalen och äter mat med kvaliten {food}')

            """för varje arbetare som äter tas en enhet mat bort, och flyttar arbetaren till road 2"""
            if eating_worker.current_life < 100:
                if int(food.quality) >= 2:
                    eating_worker.increase_life()
                else:
                    eating_worker.decrease_life()
            else:
                if int(food.quality) == 1:
                    eating_worker.decrease_life()
                else:
                    eating_worker.current_life = 100

            self._worker_out.worker_in(eating_worker)

            print(f'Arbetare med {eating_worker} i livskraft flyttades till Road2')


class Field:
    """Klassen tar in en arbetare från Road() och returnerar en enhet mat"""

    def __init__(self):

        self.fld_worker_in = None
        self.fld_worker_out = None
        self.food_road = None

    def field_road_in(self, road):
        self.fld_worker_in = road

    def field_road_out(self, road):
        self.fld_worker_out = road

    def field_food_road(self, road):
        self.food_road = road

    def create_food(self):
        return Food()

    def simulation_step(self):
        """simulering som hämtar en arbetare från r1 och skickar en enhet mat till b1"""
        if self.fld_worker_in.has_worker():
            worker = self.fld_worker_in.worker_out()
            food = self.create_food()
            self.food_road.barn_food_in(food)
            self.fld_worker_out.worker_in(worker)
        else:
            print('There is no one on the road!')


class Barn:
    """tar in mat från Food() och returnerar till DinningHall()"""

    def __init__(self):
        self.inventory = []

    def __len__(self):
        return len(self.inventory)

    def is_food(self):
        return len(self.inventory) > 0

    def barn_food_out(self):
        value = self.inventory.pop(0)
        return value

    def barn_food_in(self, food):
        self.inventory.append(food)


class Food:
    """tar in en enehet mat från Field() och returnerar till Barn()"""

    def __init__(self):
        self.quality = random.randint(1, 3)

    def food_quality(self):
        self.quality = random.randint(1, 3)

    def __str__(self):
        return str(self.quality)

    def food(self):
        return int(self.quality)


class Worker:

    def __init__(self):
        self.current_life = 100

    def __str__(self):
        return str(self.current_life)

    def decrease_life(self):
        self.current_life = max(self.current_life - random.randint(1, 4), 0)

    def increase_life(self):
        self.current_life = min(self.current_life + random.randint(1, 4), 100)

    def getworker(self):
        return self.current_life


class House:
    """Tar in en produkt och returnerar en arbetare"""

    def __init__(self):
        self.people = []
        self._road_in = None
        self._road_out = None
        self._prod_road = None

    def road_in(self, road):
        self._road_in = road

    def road_out(self, road):
        self._road_out = road

    def product_in(self, road):
        self._prod_road = road

    def simulation_step(self):
        worker = self._road_in.worker_out()
        product = self._prod_road.strg_pro_out()
        if self._road_in.has_worker():
            if random.randint(1, 5) > 3:
                for _ in range(2):
                    self.people.append(self._road_in.worker_out())
                self.people.append(Worker())

                print(f'Arbetare med livskraft {self.people[0]} och {self.people[1]} konsumerar en {product}\n'
                      f'och producerar en arbetare med {self.people[2]}')
            else:
                worker.increase_life()
                self.people.append(worker)
                print(f'Arbetare med livskraft {self.people[0]} konsumerar en {product}')
        else:
            print('The road is empty!')

        for person in self.people:
            self._road_out.worker_in(person)


class Storage:
    """tar in enhet från Produkt() och returnerar till House()"""

    def __init__(self):
        self.products = []

    def __len__(self):
        return len(self.products)

    def __str__(self):
        return f'lager'

    def strg_pro_in(self, product):

        self.products.append(product)

    def strg_pro_out(self):
        return self.products.pop(0)

    def get_strg(self):
        return self.products


class Factory:
    """Tar in en arbetare och returnerar en produkt"""

    def __init__(self):

        self.fct_road_in = None
        self.fct_road_out = None
        self.fct_prd_road = None

    def fact_road_in(self, road):
        self.fct_road_in = road

    def fact_road_out(self, road):
        self.fct_road_out = road

    def create_product(self):
        return Product()

    def fact_product_road(self, road):
        self.fct_prd_road = road

    def simulation_step(self):

        if self.fct_road_in.has_worker():
            worker = self.fct_road_in.worker_out()
            product = self.create_product()
            self.fct_prd_road.strg_pro_in(product)
            print(f'arbetare med: {worker} i livskraft går från \n '
                  f'Road1 till fabriken och tillverkar en {product} och skickar den till {self.fct_prd_road}')
            '''20 % risk att arbterare dör'''
            if random.randint(1, 5) > 3:
                self.fct_road_out.worker_in(worker)
                print(f'arbetare med {worker} i livskraft går sedan till road1')
            else:
                worker.current_life = 0
                self.fct_road_out.worker_in(worker)
                print(f'arbetare med {worker} i livskraft dog')
        else:
            print('There is no one on the road!')


class Product:
    def __init__(self):
        pass

    def __str__(self):
        return f'Produkt'


if __name__ == "__main__":
    r1 = Road()
    r2 = Road()
    d1 = DinningHall()
    b1 = Barn()
    f1 = Field()
    fa1 = Factory()
    s1 = Storage()
    h1 = House()

    for i in range(4):
        r1.worker_in(Worker())

    for i in range(2):
        s1.strg_pro_in(Product())

    #for i in range(4):
        #b1.barn_food_in(Food())

    d1.set_worker_in(r1)
    d1.set_worker_out(r2)
    d1.food_in(b1)

    f1.field_road_in(r1)
    f1.field_road_out(r1)
    f1.field_food_road(b1)

    fa1.fact_road_in(r1)
    fa1.fact_road_out(r1)
    fa1.fact_product_road(s1)

    h1.road_in(r1)
    h1.road_out(r2)
    h1.product_in(s1)
    #f1.simulation_step()
    #d1.simulation_step()
    #fa1.simulation_step()



    h1.simulation_step()
    print(r1.get_list())
    print(h1.people)
    print(r2.get_list())
















