import random
import datetime
import json
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

class System:
    def __init__(self):
        self.__review_list = []
        self.__transaction_list = []
        self.__stock = kfc_stock
        self.__user_list = []
        self.__coupon_list = []
        self.__payment_method_list = []

    def add_food_to_food_list(self,food):
        self.__stock.food_list.append(food)
        return self.__stock
    
    def add_coupon(self,coupon):
        self.__coupon_list.append(coupon)
        return self.__coupon_list

    def search_transaction_by_member_id(self,member_id):
        this_member_transaction = []
        for transaction in self.__transaction_list:
            if transaction.member_id == member_id:
                this_member_transaction.append(transaction)
        return this_member_transaction  
    
    def add_review_to_review_list(self,review):
        self.__review_list.append(review)
        return "Success"

    def search_member_by_id(self,id):
        for member in self.__user_list:
            if member.id == id:
                return member
    
    def open_menu(self):
        Menu=kfc_stock.open_menu()
        return Menu
        
    def add_member_to_user_list(self, Member):
        self.__user_list.append(Member)
    
    def add_transaction_to_transaction_list(self,transaction):
        self.__transaction_list.append(transaction)

    def add_payment_method_to_payment_method_list(self,payment_method):
        if isinstance(payment_method,PaymentMethod):
            self.__payment_method_list.append(payment_method)
        else:
            return "parameter is not Payment Method"
    
    def show_all_review(self):
        dictionary = {}
        for review in self.__review_list:   
            dictionary[review.number] = {"score":review.score,"comment":review.comment}    
        return dictionary
    
    def show_address(self,id):
        member = self.search_member_by_id(id)
        dictionary = {}  
        for address in enumerate(member.address_list):
            dictionary[address[1].name] = {"Country": address[1].country,
                                                "City": address[1].city,
                                                "District": address[1].district,
                                                "Subdistrict": address[1].subdistrict,
                                                "Road": address[1].road,
                                                "House Number": address[1].house_number,
                                                "Zip Code": address[1].zip_code,
                                                "Type": address[1].type,
                                                "Landmark": address[1].landmark,
                                                "Note": address[1].note}    
        return dictionary
    
    def show_transaction(self,id):
        transaction_list =self.search_transaction_by_member_id(id)
        dictionary = {}
        for transaction in enumerate(transaction_list):
            dictionary[f'transaction number = {transaction[0]+1}']= {"member id": id, "Transaction id":transaction[1].transaction_id, "cost":transaction[1].payment.order.total_price,"payment method":transaction[1].payment.payment_method,"delivery address":transaction[1].payment.address.address_name, "Date":transaction[1].date_time}    
        return  dictionary
    

    def show_summary(self,member_id):
        kfc_stock.show_summary(member_id)
        summary_list = self.search_member_by_id(member_id).temp_summary
        print(summary_list)
        main_item = summary_list[0]
        print(main_item)
        summary_dict = {}        
        if isinstance(main_item,Food):
            if isinstance(main_item,Food):
                if isinstance(main_item,Chicken):
                    summary_dict[main_item.get_name] = {"part" : main_item.get_part,"recipe" : main_item.get_recipe}
                elif isinstance(main_item,Drinks):
                    summary_dict[main_item.get_name] = {"size" : main_item.get_size}
                elif isinstance(main_item,Snack):
                    summary_dict[main_item.get_name] = {"categlorey" : main_item.get_categlory}
                elif isinstance(main_item,Bowl):
                    summary_dict[main_item.get_name] = {"topping" : main_item.get_topping}
        elif isinstance(main_item,Boxset):
            boxset_dict = {}
            for food in summary_list[1]:
                if isinstance(food,Food):
                    if isinstance(food,Chicken):
                        boxset_dict[str(len(boxset_dict)+1) +food.get_name] = {"part" : food.get_part,"recipe" : food.get_recipe}
                    elif isinstance(food,Drinks):
                        boxset_dict[str(len(boxset_dict)+1) +food.get_name] = {"size" : food.get_size}
                    elif isinstance(food,Snack):
                        boxset_dict[str(len(boxset_dict)+1) +food.get_name] = {"categlorey" : food.get_categlory}
                    elif isinstance(food,Bowl):
                        boxset_dict[str(len(boxset_dict)+1) +food.get_name] = {"topping" : food.get_topping}
            summary_dict[main_item.get_name] = boxset_dict
        elif isinstance(main_item,Promotion):
            promotion_dict = {}
            for item in summary_list[1]:
                if isinstance(item[0],Boxset):
                    boxset_dict = {}
                    for food in item[1]:
                        if isinstance(food,Food):
                            if isinstance(food,Chicken):
                                boxset_dict[str(len(boxset_dict)+1) +food.get_name] = {"part" : food.get_part,"recipe" : food.get_recipe}
                            elif isinstance(food,Drinks):
                                boxset_dict[str(len(boxset_dict)+1) +food.get_name] = {"size" : food.get_size}
                            elif isinstance(food,Snack):
                                boxset_dict[str(len(boxset_dict)+1) +food.get_name] = {"categlorey" : food.get_categlory}
                            elif isinstance(food,Bowl):
                                boxset_dict[str(len(boxset_dict)+1) +food.get_name ] = {"topping" : food.get_topping}
                    promotion_dict[str(len(promotion_dict)+1) + item[0].get_name] = boxset_dict
                elif isinstance(item[0],Food):
                    food_dict = {}
                    if isinstance(item[0],Chicken):
                        food_dict[item[0].get_name] = {"part" : item[0].get_part,"recipe" : item[0].get_recipe}
                    elif isinstance(item[0],Drinks):
                        food_dict[item[0].get_name] = {"size" : item[0].get_size}
                    elif isinstance(item[0],Snack):
                        food_dict[item[0].get_name] = {"categlorey" : item[0].get_categlory}
                    elif isinstance(item[0],Bowl):
                        food_dict[item[0].get_name] = {"topping" : item[0].get_topping}
                    promotion_dict[str(len(promotion_dict)+1) + item[0].get_name] = food_dict
            summary_dict[str(len(summary_dict)+1) + main_item.get_name] = promotion_dict
            summary_dict["price"] = main_item.get_price
        return summary_dict
                    
    def member_add_to_cart(self,member_id):
        dictionary = {}
        member_cart = self.search_member_by_id(member_id).add_to_cart()
        dictionary[self.search_member_by_id(member_id).name] = {"amount" : len(member_cart.meal_list), "total price" : member_cart.total_price}
        return dictionary
    
    def member_show_cart(self,member_id):
        dictionary = {}
        member_cart = self.search_member_by_id(member_id).show_cart()
        detail_dict = {}
        for item in member_cart:
            detail_dict[item.get_name] = { "price" : item.get_price ,"item_id": item.id}
        dictionary[self.search_member_by_id(member_id).name + " Cart"] = detail_dict
        return dictionary
    
    def check_out(self,member_id):
        member_order = self.search_member_by_id(member_id).cart.check_out(member_id)
        dictionary = {"order_id" : member_order.order_id, "date-time" : member_order.date_time}
        meal_dict = {}
        if isinstance(member_order,Order):
            for meal in member_order.item_list:
                meal_dict[meal.get_name] = {"price":meal.get_price}
            dictionary[member_order.order_id] = meal_dict
        else:
            dictionary[member_order] = "cannot check out"
        return dictionary
    
    def use_coupon(self,member_id,coupon_id):
        dictionary = {}
        this_order = self.search_member_by_id(member_id).temp_order.use_coupon(coupon_id)
        if isinstance(this_order,Order):
            dictionary["order_id"] = this_order.order_id
            dictionary["current_price"] = this_order.total_price + this_order.discount
            dictionary["used_coupon"] = coupon_id
            dictionary["discount_price"] = this_order.discount
            dictionary["total_price"] = this_order.total_price
            return dictionary
        else:
            dictionary["error"] = "cannot use coupon"
            return dictionary
    
    def show_payment(self,member_id):
        dictionary = {}
        dictionary["member_id"] = member_id
        dictionary["order_id"] = self.search_member_by_id(member_id).temp_payment.order.order_id
        meal_dict = {}
        for item in self.search_member_by_id(member_id).temp_payment.order.item_list:
            meal_dict[str(len(meal_dict)+1) + item.get_name] = item.get_price
        dictionary["order_item"] = meal_dict
        if self.search_member_by_id(member_id).temp_payment.payment_method == None:
            dictionary["payment_method"] = self.search_member_by_id(member_id).temp_payment.payment_method
        else:
            dictionary["payment_method"] = self.search_member_by_id(member_id).temp_payment.payment_method.payment_method_name
        dictionary["Address"] = self.search_member_by_id(member_id).temp_payment.address
        return dictionary
    
    def open_menu(self):
        dictionary = {}
        menu_list = self.__stock.menu_recipe()
        alacarte_dict = {}
        boxset_dict = {}
        promotion_dict = {}
        for item in menu_list[0]:
            alacarte_dict[item.get_name] = {"price" : item.get_price}
        for item in menu_list[1]:
            boxset_dict[item.get_name] = {"price" : item.get_price}
        for item in menu_list[2]:
            promotion_dict[item.get_name] = {"price" : item.get_price}
        dictionary["a la carte"] = alacarte_dict
        dictionary["box set"] = boxset_dict
        dictionary["promotion"] = promotion_dict
        return dictionary
    
    def remove_coupon(self,coupon):
        if coupon in self.__coupon_list:
            self.__coupon_list.remove(coupon)
    
    
    @property
    def coupon_list(self):
        return self.__coupon_list
    @property
    def review_list(self):
        return self.__review_list
    @property
    def user_list(self):
        return self.__user_list
    @property
    def payment_method_list(self):
        return self.__payment_method_list
    @property
    def stock(self):
        return self.__stock
    
    @property
    def transaction_list(self):
        return self.__transaction_list

        
########################################################################
class Review:
    def __init__(self,score,comment):
        self.__review_number = len(KFC1.review_list)+1
        self.__score = score
        self.__comment = comment
    
    @property
    def comment(self):
        return self.__comment
    @property
    def score(self):
        return self.__score
    @property
    def number(self):
        return self.__review_number
    
########################################################################
class User:
    def __init__(self):
        pass

    def open_menu(self):
        KFC1.open_menu()

########################################################################
class Guest(User):
    def __init__(self):
        self.__guest_id = "G" + str(random.randint(1000,9999))
        # self.__username = None        
        # self.__password = None
    
    def show_review_list(self):
        list=[]
        ReviewList=KFC1.review_list
        for review in ReviewList:
            list.append(review.comment)
        return list
    
    def register(self, name, username, password):
        user_list=KFC1.user_list
        for member in user_list:
            if isinstance(member, Member) and username==member.username:
                return "Error"
        member_cart = Cart()
        new_member=Member(username, password, str(len(user_list)+1), name,member_cart)
        KFC1.add_member_to_user_list(new_member)
        return new_member
        
    def login(self, Username, Password):
        UserList=KFC1.user_list
        for member in UserList:
            if isinstance(member, Member):
                if Username==member.username and Password==member.password:
                    return member
        return "Error"   

    @property
    def id(self):
        return self.__guest_id  
    @property    
    def username(self):
        return self.__username
    @property
    def password(self):
        return self.__password

########################################################################
class Member(User):
    def __init__(self,username,passward,id,name,cart):
        self.__username = username
        self.__passward = passward
        self.__member_id = id
        self.__member_name = name
        self.__address_list = []
        self.__cart = cart
        self.__temp_selected = None
        self.__temp_order = None
        self.__temp_payment = None
        self.__temp_summary = None

    def add_to_cart(self):
        self.__cart.add_items(self.__temp_summary[0])
        self.__temp_summary = None
        return self.__cart
    
    def remove_from_cart(self,item_id):
        self.__cart.remove_items(KFC1.stock.search_meals_by_id(item_id))
        return self.__cart
    
    def show_cart(self):
        return self.cart.meal_list

    def write_review(self,score,comment):
        new_review = Review(score,comment)
        KFC1.add_review_to_review_list(new_review)
        return "Success"
        
    def add_address(self,address_name, new_address): #new_address เป็น list
        self.__address_list.append(Address(address_name,new_address))

    def remove_address(self,address_for_delete_name):
        for address in self.__address_list:
            if address.address_name == address_for_delete_name:
                self.__address_list.remove(address)
        return self.__address_list

    def show_my_transaction(self):
        my_transaction = KFC1.search_transaction_by_member_id(self.__member_id)
        return my_transaction
        
    def create_payment(self):
        self.__temp_payment = Payment(self.__temp_order)
        return self.__temp_payment
    
    def show_temp_selected(self):
        if self.__temp_selected!= None:
            dictionary = {}
            if isinstance(self.__temp_selected,Promotion):
                item_in_promotion_dict = {}
                for item in self.__temp_selected.item_in_promotion:
                    if isinstance(item,Boxset):
                        food_in_boxset_dict = {}
                        for food in item.get_food_in_boxset_list:
                            food_in_boxset_dict[str(len(food_in_boxset_dict)+1)+food.get_name] = KFC1.stock.show_food_detail_in_dictionary(food)
                        item_in_promotion_dict[str(len(item_in_promotion_dict)+1)+item.get_name] = food_in_boxset_dict
                    if isinstance(item,Food):
                        item_in_promotion_dict[str(len(item_in_promotion_dict)+1)+item.get_name] = KFC1.stock.show_food_detail_in_dictionary(item)
                dictionary[self.__temp_selected.get_name] = item_in_promotion_dict
            elif isinstance(self.__temp_selected,Boxset):
                food_in_boxset_dict = {}
                for food in self.__temp_selected.get_food_in_boxset_list:
                    food_in_boxset_dict[str(len(food_in_boxset_dict)+1)+food.get_name] = KFC1.stock.show_food_detail_in_dictionary(food)
                dictionary[self.__temp_selected.get_name] = food_in_boxset_dict
            elif isinstance(self.__temp_selected,Food):
                dictionary[self.__temp_selected.get_name] = KFC1.stock.show_food_detail_in_dictionary(self.__temp_selected)
        return dictionary
                    

        
    @property
    def username(self):
        return self.__username
    
    @property
    def password(self):
        return self.__passward
    
    @property
    def id(self):
        return self.__member_id
    
    @property
    def address_list(self):
        return self.__address_list
    
    @property
    def temp_selected(self):
        return self.__temp_selected
    
    @property
    def temp_summary(self):
        return self.__temp_summary
    
    @property
    def temp_order(self):
        return self.__temp_order
    
    @property
    def temp_payment(self):
        return self.__temp_payment
    
    @property
    def name(self):
        return self.__member_name

    @property
    def cart(self):
        return self.__cart
    
    def set_temp_summary(self,new_summary):
        self.__temp_summary = new_summary

    def set_temp_selected(self,selected_meal):
        self.__temp_selected = selected_meal

    def set_temp_payment(self,payment):
        self.__temp_payment = payment

    def set_temp_order(self,order):
        self.__temp_order = order

########################################################################
class Food:
    def __init__(self,price,name,id):
        self.__price = price
        self.__food_name = name
        self.__food_id = id
        self.__food_type = None

    @property
    def get_food_type(self):
        return self.__food_type

    @property
    def get_name(self):
        return self.__food_name
    
    @property
    def id(self):
        return self.__food_id
    
    @property
    def get_price(self):
        return self.__price
    

########################################################################
class Chicken(Food):
    def __init__(self, price, name, part, recipe,id):
        super().__init__(price,name,id)
        self.__food_type = "Chicken"
        self.__part = part
        self.__recipe = recipe


    @property
    def get_part(self):
        return self.__part
    
    @property
    def get_recipe(self):
        return self.__recipe
    
    @property
    def get_detail(self):
        return self.__detail

########################################################################
class Drinks(Food):
    def __init__(self, price, name, size, id):
        super().__init__(price,name, id)
        self.__food_type = "Drinks"
        self.__size = size

    @property
    def get_size(self):
        return self.__size

########################################################################
class Snack(Food):
    def __init__(self, price, name, snack_category,id):
        super().__init__(price,name,id)
        self.food_type = "Snack"
        self.__categlory = snack_category

    @property
    def get_categlory(self):
        return self.__categlory

########################################################################
class Bowl(Food):
    def __init__(self, price, name, topping,id):
        super().__init__(price,name,id)
        self.__food_type = "Bowl"
        self.__topping = topping

    @property
    def get_topping(self):
        return self.__topping

########################################################################
class Boxset:
    def __init__(self,name,food_list,price,id):
        self.__set_name = name
        self.__food_in_boxset_list = food_list
        self.__set_price = price
        self.__boxset_id = id
        
    @property
    def get_food_in_boxset_list(self):
        return self.__food_in_boxset_list
    
    @property
    def get_name(self):
        return self.__set_name
    
    @property
    def id(self):
        return self.__boxset_id
    
    @property
    def get_price(self):
        return self.__set_price
########################################################################
class Promotion:
    def __init__(self,name,boxset_list,price,id):
        self.__set_name = name
        self.__boxset_in_promotion_list = boxset_list
        self.__price = price
        self.__promotion_id = id

    @property
    def id(self):
        return self.__promotion_id
        
    @property
    def get_price(self):
        return self.__price
    
    @property
    def get_name(self):
        return self.__set_name
    
    @property
    def item_in_promotion(self):
        return self.__boxset_in_promotion_list
    
########################################################################
class Stock:
    def __init__(self):
        self.__food_list = []
        self.__boxset_list = []
        self.__promotion_list = []
        self.__food_recipe=[]
        self.__boxset_recipe=[]
        self.__promotion_recipe=[]
            
    def search_meals_by_id(self,id):
        all_list = self.__food_list + self.__boxset_list + self.__promotion_list
        for item in all_list:
            if item.id == id:
                return item
        return "not found"
    
    def search_meal_by_name(self, name):
        all_list = self.__food_list + self.__boxset_list + self.__promotion_list
        for item in all_list:
            if item.get_name == name:
                return item

    def show_food_detail_in_dictionary(self,meal_instance):
        dictionary = {}
        if isinstance(meal_instance, Chicken):
            dictionary[meal_instance.get_name] = {"price":meal_instance.get_price, "part": meal_instance.get_part, "recipe": meal_instance.get_recipe}
        elif isinstance(meal_instance, Drinks):
            dictionary[meal_instance.get_name] = {"price": meal_instance.get_price, "size": meal_instance.get_size}
        elif isinstance(meal_instance, Snack):
            dictionary[meal_instance.get_name] = {"price": meal_instance.get_price, "categlory": meal_instance.get_categlory}
        elif isinstance(meal_instance, Bowl):
            dictionary[meal_instance.get_name] = {"price": meal_instance.get_price, "topping": meal_instance.get_topping}
        dictionary["id"] = meal_instance.id
        return dictionary
                    
    def select_food(self,memebr_id,meal_name):
        wanted_meal = self.search_meal_by_name(meal_name)
        KFC1.search_member_by_id(memebr_id).set_temp_selected(wanted_meal)
        food_slected = KFC1.search_member_by_id(memebr_id).temp_selected
        dictionary = {}  
        if isinstance(food_slected, Food):
            # dictionary = self.show_food_detail_in_dictionary(food_slected)
            dictionary[food_slected.get_name] = self.show_food_detail_in_dictionary(food_slected)
        elif isinstance(food_slected, Boxset):
            food_in_boxset_dictionary = {}
            for food in food_slected.get_food_in_boxset_list:
                food_in_boxset_dictionary[str(len(food_in_boxset_dictionary)+1)+food.get_name] = self.show_food_detail_in_dictionary(food)
            dictionary[food_slected.get_name] = food_in_boxset_dictionary
        elif isinstance(food_slected, Promotion):
            for item in food_slected.item_in_promotion:
                if isinstance(item, Boxset):
                    item_in_promotion_dictionary = {}
                    food_in_boxset_dictionary = {}
                    for food in item.get_food_in_boxset_list:
                        food_in_boxset_dictionary[str(len(food_in_boxset_dictionary)+1)+food.get_name] = self.show_food_detail_in_dictionary(food)
                    item_in_promotion_dictionary[str(len(item_in_promotion_dictionary)+1)+item.get_name] = food_in_boxset_dictionary
                if isinstance(item, Food):
                    item_in_promotion_dictionary[str(len(item_in_promotion_dictionary)+1)+item.get_name] = self.show_food_detail_in_dictionary(item)
            dictionary[food_slected.get_name] = item_in_promotion_dictionary
        return dictionary
    
    def search_food_by_attribute(self,attribute1,attribute2):
        for food in self.__food_list:
            if isinstance(food,Chicken) and food.get_part == attribute1 and food.get_recipe == attribute2:
                return food
            elif isinstance(food,Drinks) and food.get_name == attribute1 and food.get_size == attribute2:
                return food
            elif isinstance(food,Snack) and food.get_name == attribute1 and food.get_categlory == attribute2:
                return food
            elif isinstance(food,Bowl) and food.get_name == attribute1 and food.get_topping == attribute2:
                return food
        return "not found"


    def modify_food(self,member_id,modify_food_id,attribute1,attribute2):
        wanted_food = KFC1.search_member_by_id(member_id).temp_selected
        if isinstance(wanted_food, Promotion):
            for item in wanted_food.item_in_promotion:
                if isinstance(item, Boxset):
                    for food in item.get_food_in_boxset_list:
                        if food.id == modify_food_id:
                            item.get_food_in_boxset_list.remove(food)
                            item.get_food_in_boxset_list.append(self.search_food_by_attribute(attribute1,attribute2))
                            KFC1.search_member_by_id(member_id).set_temp_selected(wanted_food)
                            return wanted_food
                if isinstance(item, Food):
                    if item.id == modify_food_id:
                        wanted_food.item_in_promotion.remove(item)
                        wanted_food.item_in_promotion.append(self.search_food_by_attribute(attribute1,attribute2))
                        KFC1.search_member_by_id(member_id).set_temp_selected(wanted_food)
                        return wanted_food
        elif isinstance(wanted_food, Boxset):
            for food in wanted_food.get_food_in_boxset_list:
                if food.id == modify_food_id:
                    wanted_food.get_food_in_boxset_list.remove(food)
                    wanted_food.get_food_in_boxset_list.append(self.search_food_by_attribute(attribute1,attribute2))
                    KFC1.search_member_by_id(member_id).set_temp_selected(wanted_food)
                    return wanted_food
        elif isinstance(wanted_food, Food):
            if wanted_food.id == modify_food_id:
                KFC1.search_member_by_id(member_id).set_temp_selected(self.search_food_by_attribute(attribute1,attribute2))
                return wanted_food

    def check_stock(self,food):
        for item in self.__food_list:
            if food.id == item.id:
                return True
        return False
    
    def remove_food_from_stock(self,food):
        if food in self.__food_list:
            self.__food_list.remove(food)
                

    def show_summary(self,member_id):
        summary_list = [KFC1.search_member_by_id(member_id).temp_selected]
        if isinstance(summary_list[0],Promotion):
            item_in_promotion = []
            for item in summary_list[0].item_in_promotion:
                if isinstance(item,Boxset):
                    boxset_detail = [item]
                    food_in_boxset = []
                    for food in item.get_food_in_boxset_list:
                        food_in_boxset.append(food)
                    boxset_detail.append(food_in_boxset)
                    item_in_promotion.append(boxset_detail)
                elif isinstance(item,Food):
                    boxset_detail = [item]
                    item_in_promotion.append(boxset_detail)
            summary_list.append(item_in_promotion)
        elif isinstance(summary_list[0],Boxset):
            food_in_boxset = []
            for food in summary_list[0].get_food_in_boxset_list:
                food_in_boxset.append(food)
            summary_list.append(food_in_boxset)
        elif isinstance(summary_list[0],Food):
            pass
        KFC1.search_member_by_id(member_id).set_temp_summary(summary_list),
        return summary_list
                           
    def menu_recipe(self):
        menu_list=[[], [], []]
        for food in self.food_recipe:
            menu_list[0].append(food)
        for boxset in self.boxset_recipe:
            menu_list[1].append(boxset)
        for promotion in self.promotion_recipe:
            menu_list[2].append(promotion)
        return menu_list
            
    def add_to_stock(self, instance):
        if isinstance(instance, Food):
            self.food_list.append(instance)
        elif isinstance(instance, Boxset):
            self.boxset_list.append(instance)
        elif isinstance(instance, Promotion):
            self.promotion_list.append(instance)
             
    def add_recipe(self, Instance):
        if isinstance(Instance, Food):
            self.food_recipe.append(Instance)
        elif isinstance(Instance, Boxset):
            self.boxset_recipe.append(Instance)
        elif isinstance(Instance, Promotion):
            self.promotion_recipe.append(Instance)  
    @property
    def food_list(self):
        return self.__food_list
    @property
    def boxset_list(self):
        return self.__boxset_list
    @property
    def promotion_list(self):
        return self.__promotion_list
    @property
    def food_recipe(self):
        return self.__food_recipe
    @property
    def boxset_recipe(self):
        return self.__boxset_recipe
    @property
    def promotion_recipe(self):
        return self.__promotion_recipe


########################################################################
class Cart:
    def __init__(self):
        self.__meal_list = []
        self.__total_price = 0

    def add_items(self,item):
        self.__meal_list.append(item)
        self.__total_price += item.get_price
        return "success"

    def remove_items(self,item):
        self.meal_list.remove(item)
        self.__total_price -= item.get_price
        return "success"
    
    def create_order(self,item_list,price,member_id):
        member = KFC1.search_member_by_id(member_id)
        id = f"{member_id}" + F"{len(member.show_my_transaction())}"
        date = f"{datetime.date.today()}"
        order = Order(id,item_list,date,price,used_coupon=None)
        member.set_temp_order(order)
        return id
        
    
    def check_out(self,member_id): #checkวาของมีในstockแล้วสร้างorder
        for meal in self.__meal_list:
            if isinstance(meal,Promotion):
                for box in meal.item_in_promotion:
                    if isinstance(box,Boxset):
                        for food in box.get_food_in_boxset_list:
                            if kfc_stock.check_stock(food) == False:
                                return f"{meal.get_name} is out of stock"
                    if isinstance(box,Food):
                        if kfc_stock.check_stock(box) == False:
                            return f"{meal.get_name} is out of stock"
            elif isinstance(meal,Boxset):
                for food in meal.get_food_in_boxset_list:
                    if  kfc_stock.check_stock(food) == False:
                        return f"{meal.get_name} is out of stock"
            elif  isinstance(meal,Food):
                if kfc_stock.check_stock(meal) == False:
                    return f"{meal.get_name} is out of stock"
        self.create_order(self.__meal_list,self.__total_price,member_id)
        KFC1.search_member_by_id(member_id).set_temp_payment(Payment(KFC1.search_member_by_id(member_id).temp_order))
        return KFC1.search_member_by_id(member_id).temp_order
    
    @property
    def meal_list(self):
        return self.__meal_list
    
    @meal_list.setter
    def meal_list(self,meal):
        self.__meal_list.append(meal)
        return self.__meal_list

    @property
    def total_price(self):
        return self.__total_price
#########################################################################
class Coupon:
    def __init__(self,code,discount):
        self.__coupon_code = code
        self.__coupon_discount = discount


    @property 
    def coupon_code(self):
        return self.__coupon_code
    
    @property 
    def coupon_discount(self):
        return self.__coupon_discount


#########################################################################
class Order:
    def __init__(self,id,item_list,date,price,used_coupon):
        self.__used_coupon = used_coupon
        self.__items_list = item_list
        self.__order_id = id
        self.__date = date
        self.__total_price = price
        self.__discount = None
    
    def check_coupon(self,code):
        for coupon in KFC1.coupon_list:
            if coupon.coupon_code == code:
                return coupon  
        return False

    def use_coupon(self,coupon_code):
        if self.__used_coupon == None and self.check_coupon(coupon_code):
            self.__used_coupon = self.check_coupon(coupon_code)
            self.__discount = self.check_coupon(coupon_code).coupon_discount*self.__total_price
            self.__total_price -= self.__discount
            return self
        else:
            return False

    def used_coupon(self):
        return self.__used_coupon
    @property
    def item_list(self):
        return self.__items_list
    
    @property
    def order_id(self):
        return self.__order_id
    
    @property
    def date_time(self):
        return self.__date
    
    @property
    def total_price(self):
        return self.__total_price
    
    @property
    def discount(self):
        return self.__discount
#########################################################################
class Address:
    def __init__(self,address_name,address_list):
        self.__address_name = address_name
        self.__country = address_list[0]
        self.__city = address_list[1]
        self.__district = address_list[2]
        self.__subdistrict = address_list[3]
        self.__road = address_list[4]
        self.__house_number = address_list[5]
        self.__zip_code = address_list[6]
        self.__type = address_list[7]
        self.__landmark = address_list[8]
        self.__note = address_list[9]

    @property
    def name(self):
        return self.__address_name
    @property
    def country(self):
        return self.__country
    @property
    def city(self):
        return self.__city
    @property
    def district(self):
        return self.__district
    @property
    def subdistrict(self):
        return self.__subdistrict
    @property
    def road(self):
        return self.__road
    @property
    def house_number(self):
        return self.__house_number
    @property
    def zip_code(self):
        return self.__zip_code
    @property
    def type(self):
        return self.__type
    @property
    def landmark(self):
        return self.__landmark
    @property
    def note(self):
        return self.__note
    @property
    def address_name(self):
        return self.__address_name

##########################################################################
class Payment:
    def __init__(self,order):
        self.__order = order
        self.__address = None
        self.__payment_method = None

    def select_payment_method(self,payment_method_name):
        for payment_method in KFC1.payment_method_list:
            if payment_method.payment_method_name == payment_method_name: #("credit_card","pay_on_delivery","qr_code")
                self.__payment_method = payment_method
                return self.__payment_method
        return "Error"
    
    def select_address(self,member_id,address_name):
        for address in KFC1.search_member_by_id(member_id).address_list:
            if address.address_name == address_name:
                self.__address = address
                return self.__address

    def payment_success(self,member):
        transaction_id = f"{member.id}" + f"{(member.temp_payment.order.order_id)}"
        KFC1.add_transaction_to_transaction_list(Transaction(member.id,member.temp_payment,transaction_id))
        for coupon in KFC1.coupon_list: # เอา coupon ใช้แล้วออกจาก list
            if coupon == self.__order.used_coupon:
                KFC1.remove_coupon(coupon)
        for meal in self.order.item_list: # เอา food จ่ายแล้วออกจาก stock
            if isinstance(meal,Promotion):
                for box in meal.item_in_promotion:
                    for food in box.get_food_in_boxset_list():
                        kfc_stock.remove_food_from_stock(food)
            elif isinstance(meal,Boxset):
                for food in meal.get_food_in_boxset_list():
                    kfc_stock.remove_food_from_stock(food)
            elif isinstance(meal,Food):
                kfc_stock.remove_food_from_stock(meal)
        member.set_temp_payment(None)
        member.set_temp_order(None)
        return ("payment success")
    
    @property
    def payment_method(self):
        return self.__payment_method
    
    @property
    def address(self):
        return self.__address
    
    @property
    def order(self):
        return self.__order
    

##########################################################################
class PaymentMethod:
    def __init__(self,method_name):
        self.__method_name = method_name
    
    @property
    def payment_method_name(self):
        return self.__method_name
    
##########################################################################
class Transaction:
    def __init__(self,member_id,payment,transaction_id):
        self.__member_id = member_id
        self.__payment = payment
        self.__date_time = datetime.datetime.now()
        self.__transaction_id = transaction_id
        
    @property
    def member_id(self):
        return self.__member_id    
    @property
    def payment(self):
        return self.__payment
    @property
    def date_time(self):
        return self.__date_time
    @property
    def transaction_id(self):
        return self.__transaction_id

##########################################################################
### stock instance
kfc_stock = Stock()
###System instance
KFC1 = System()
###Payment method instance
pay_by_qr_code = PaymentMethod("qr_code")
KFC1.add_payment_method_to_payment_method_list(pay_by_qr_code)
pay_by_credit_card = PaymentMethod("credit_card")
KFC1.add_payment_method_to_payment_method_list(pay_by_credit_card)
pay_on_delivery =PaymentMethod("pay_on_delivery")
KFC1.add_payment_method_to_payment_method_list(pay_on_delivery)
###instance member
id1 = Guest()
id1.register("Warchot inkun","IQnaja","warachot2")

#Warachot = Member("IQnaja","warachot2","0001","Warchot inkun",)  

###Stock instance

### Chicken Instances
chicken_recipe=Chicken(50, "ไก่ทอด", None, None, None)
kfc_stock.add_recipe(chicken_recipe)
chicken1 = Chicken(50, "ไก่ทอด", "อก", "ออริจินอล","001")
chicken2 = Chicken(50, "ไก่ทอด", "อก", "ออริจินอล", "002")
chicken3 = Chicken(50, "ไก่ทอด", "อก", "สไปซี่", "003")
chicken4 = Chicken(50, "ไก่ทอด", "อก", "สไปซี่", "004")
chicken5 = Chicken(50, "ไก่ทอด", "อก", "ไม่กรอบ", "005")
chicken6 = Chicken(50, "ไก่ทอด", "อก", "ไม่กรอบ", "006")
chicken7 = Chicken(50, "ไก่ทอด", "น่อง", "ออริจินอล", "007")
chicken8 = Chicken(50, "ไก่ทอด", "น่อง", "ออริจินอล", "008")
chicken9 = Chicken(50, "ไก่ทอด", "น่อง", "สไปซี่", "009")
chicken10 = Chicken(50, "ไก่ทอด", "น่อง", "สไปซี่", "010")
chicken11 = Chicken(50, "ไก่ทอด", "น่อง", "ไม่กรอบ", "011")
chicken12 = Chicken(50, "ไก่ทอด", "น่อง", "ไม่กรอบ", "012")
chicken13 = Chicken(50, "ไก่ทอด", "สะโพก", "ออริจินอล", "013")
chicken14 = Chicken(50, "ไก่ทอด", "สะโพก", "ออริจินอล", "014")
chicken15 = Chicken(50, "ไก่ทอด", "สะโพก", "สไปซี่", "015")
chicken16 = Chicken(50, "ไก่ทอด", "สะโพก", "สไปซี่", "016")
chicken17 = Chicken(50, "ไก่ทอด", "สะโพก", "ไม่กรอบ", "017")
chicken18 = Chicken(50, "ไก่ทอด", "สะโพก", "ไม่กรอบ", "018")
chicken19 = Chicken(50, "ไก่ทอด", "ปีก", "ออริจินอล", "019")
chicken20 = Chicken(50, "ไก่ทอด", "ปีก", "ออริจินอล", "020")
chicken21 = Chicken(50, "ไก่ทอด", "ปีก", "สไปซี่", "021")  
chicken22 = Chicken(50, "ไก่ทอด", "ปีก", "สไปซี่", "022")
chicken23 = Chicken(50, "ไก่ทอด", "ปีก", "ไม่กรอบ", "023")
chicken24 = Chicken(50, "ไก่ทอด", "ปีก", "ไม่กรอบ", "024")

kfc_stock.add_to_stock(chicken1)
kfc_stock.add_to_stock(chicken2)
kfc_stock.add_to_stock(chicken3)
kfc_stock.add_to_stock(chicken4)
kfc_stock.add_to_stock(chicken5)
kfc_stock.add_to_stock(chicken6)
kfc_stock.add_to_stock(chicken7)
kfc_stock.add_to_stock(chicken8)
kfc_stock.add_to_stock(chicken9)
kfc_stock.add_to_stock(chicken10)
kfc_stock.add_to_stock(chicken11)
kfc_stock.add_to_stock(chicken12)
kfc_stock.add_to_stock(chicken13)
kfc_stock.add_to_stock(chicken14)
kfc_stock.add_to_stock(chicken15)
kfc_stock.add_to_stock(chicken16)
kfc_stock.add_to_stock(chicken17)
kfc_stock.add_to_stock(chicken18)
kfc_stock.add_to_stock(chicken19)
kfc_stock.add_to_stock(chicken20)
kfc_stock.add_to_stock(chicken21)
kfc_stock.add_to_stock(chicken22)
kfc_stock.add_to_stock(chicken23)
kfc_stock.add_to_stock(chicken24)


### Drinks Instances
drink_recipe1=Drinks(20, "น้ำเปล่า", None, None)
kfc_stock.add_recipe(drink_recipe1)
drink1 = Drinks(10, "น้ำเปล่า", "S", "101")
drink2 = Drinks(10, "น้ำเปล่า", "S", "102")
drink3 = Drinks(20, "น้ำเปล่า", "M", "103")
drink4 = Drinks(20, "น้ำเปล่า", "M", "104")
drink5 = Drinks(25, "น้ำเปล่า", "L", "105")
drink6 = Drinks(25, "น้ำเปล่า", "L", "106")
drink7 = Drinks(30, "น้ำเปล่า", "XL", "107")
drink8 = Drinks(30, "น้ำเปล่า", "XL", "108")
drink_recipe2=Drinks(50, "น้ำอัดลม", None, None)
kfc_stock.add_recipe(drink_recipe2)
drink9 = Drinks(35, "น้ำอัดลม", "S", "109")
drink10 = Drinks(35, "น้ำอัดลม", "S", "110")
drink11 = Drinks(50, "น้ำอัดลม", "M", "111")
drink12 = Drinks(50, "น้ำอัดลม", "M", "112")
drink13 = Drinks(65, "น้ำอัดลม", "L", "113")
drink14 = Drinks(65, "น้ำอัดลม", "L", "114")
drink15 = Drinks(85, "น้ำอัดลม", "XL", "115")
drink16 = Drinks(85, "น้ำอัดลม", "XL", "116")

kfc_stock.add_to_stock(drink1)
kfc_stock.add_to_stock(drink2)
kfc_stock.add_to_stock(drink3)
kfc_stock.add_to_stock(drink4)
kfc_stock.add_to_stock(drink5)
kfc_stock.add_to_stock(drink6)
kfc_stock.add_to_stock(drink7)
kfc_stock.add_to_stock(drink8)
kfc_stock.add_to_stock(drink9)
kfc_stock.add_to_stock(drink10)
kfc_stock.add_to_stock(drink11)
kfc_stock.add_to_stock(drink12)
kfc_stock.add_to_stock(drink13)
kfc_stock.add_to_stock(drink14)
kfc_stock.add_to_stock(drink15)
kfc_stock.add_to_stock(drink16)

### Snack Instances
snack_recipe1=Snack(60, "เฟรนซ์ฟราย", None, None)
kfc_stock.add_recipe(snack_recipe1)
snack1 = Snack(60, "เฟรนช์ฟรายส์", "extra", "201")
snack2 = Snack(60, "เฟรนช์ฟรายส์", "extra", "202")
snack3 = Snack(60, "เฟรนช์ฟรายส์", "extra", "203")
snack4 = Snack(60, "เฟรนช์ฟรายส์", "extra", "204")
snack5 = Snack(60, "เฟรนช์ฟรายส์", "extra", "205")
snack_recipe2=Snack(100, "นักเก็ต", None, None)
kfc_stock.add_recipe(snack_recipe2)
snack6 = Snack(100, "นักเก็ต", "fries", "206")
snack7 = Snack(100, "นักเก็ต", "fries", "207")
snack8 = Snack(100, "นักเก็ต", "fries", "208")
snack9 = Snack(100, "นักเก็ต", "fries", "209")
snack10 = Snack(100, "นักเก็ต", "fries", "210")
snack_recipe3=Snack(60, "ทูน่าสลัด", None, None)
kfc_stock.add_recipe(snack_recipe3)
snack11 = Snack(60, "ทูน่าสลัด", "extra", "211")
snack12 = Snack(60, "ทูน่าสลัด", "extra", "212")
snack13 = Snack(60, "ทูน่าสลัด", "extra", "213")
snack14 = Snack(60, "ทูน่าสลัด", "extra", "214")
snack15 = Snack(60, "ทูน่าสลัด", "extra", "215")
snack_recipe4=Snack(60, "มันบด", None, None)
kfc_stock.add_recipe(snack_recipe4)
snack16 = Snack(60, "มันบด", "extra", "216")
snack17 = Snack(60, "มันบด", "extra", "217")
snack18 = Snack(60, "มันบด", "extra", "218")
snack19 = Snack(60, "มันบด", "extra", "219")
snack20 = Snack(60, "มันบด", "extra", "220")
snack_recipe5=Snack(30, "ทาร์ตไข่", None, None)
kfc_stock.add_recipe(snack_recipe5)
snack21 = Snack(30, "ทาร์ตไข่", "fries", "221")
snack22 = Snack(30, "ทาร์ตไข่", "fries", "222")
snack23 = Snack(30, "ทาร์ตไข่", "fries", "223")
snack24 = Snack(30, "ทาร์ตไข่", "fries", "224")
snack25 = Snack(30, "ทาร์ตไข่", "fries", "225")
snack_recipe6=Snack(50, "วิงซ์แซ่บ", None, None)
kfc_stock.add_recipe(snack_recipe6)
snack26 = Snack(50, "วิงซ์แซ่บ", "wingzab", "226")
snack27 = Snack(50, "วิงซ์แซ่บ", "wingzab", "227")
snack28 = Snack(50, "วิงซ์แซ่บ", "wingzab", "228")
snack29 = Snack(50, "วิงซ์แซ่บ", "wingzab", "229")
snack30 = Snack(50, "วิงซ์แซ่บ", "wingzab", "230")
snack31 = Snack(50, "วิงซ์แซ่บ", "wingzab", "231")
snack32 = Snack(50, "วิงซ์แซ่บ", "wingzab", "232")
snack33 = Snack(50, "วิงซ์แซ่บ", "wingzab", "233")
snack34 = Snack(50, "วิงซ์แซ่บ", "wingzab", "234")
snack35 = Snack(50, "วิงซ์แซ่บ", "wingzab", "235")

kfc_stock.add_to_stock(snack1)
kfc_stock.add_to_stock(snack2)
kfc_stock.add_to_stock(snack3)
kfc_stock.add_to_stock(snack4)
kfc_stock.add_to_stock(snack5)
kfc_stock.add_to_stock(snack6)
kfc_stock.add_to_stock(snack7)
kfc_stock.add_to_stock(snack8)
kfc_stock.add_to_stock(snack9)
kfc_stock.add_to_stock(snack10)
kfc_stock.add_to_stock(snack11)
kfc_stock.add_to_stock(snack12)
kfc_stock.add_to_stock(snack13)
kfc_stock.add_to_stock(snack14)
kfc_stock.add_to_stock(snack15)
kfc_stock.add_to_stock(snack16)
kfc_stock.add_to_stock(snack17)
kfc_stock.add_to_stock(snack18)
kfc_stock.add_to_stock(snack19)
kfc_stock.add_to_stock(snack20)
kfc_stock.add_to_stock(snack21)
kfc_stock.add_to_stock(snack22)
kfc_stock.add_to_stock(snack23)
kfc_stock.add_to_stock(snack24)
kfc_stock.add_to_stock(snack25)
kfc_stock.add_to_stock(snack26)
kfc_stock.add_to_stock(snack27)
kfc_stock.add_to_stock(snack28)
kfc_stock.add_to_stock(snack29)
kfc_stock.add_to_stock(snack30)
kfc_stock.add_to_stock(snack31)
kfc_stock.add_to_stock(snack32)
kfc_stock.add_to_stock(snack33)
kfc_stock.add_to_stock(snack34)
kfc_stock.add_to_stock(snack35)

### Bowl Instances
bowl_recipe1=Bowl(120, "ข้าวไก่ทอด", None, None)
kfc_stock.add_recipe(bowl_recipe1)
bowl1 = Bowl(150, "ข้าวไก่ทอด", "ไก่ทอดแกงเขียวหวาน", "301")
bowl2 = Bowl(150, "ข้าวไก่ทอด", "ไก่ทอดแกงเขียวหวาน", "302")
bowl3 = Bowl(150, "ข้าวไก่ทอด", "ไก่ทอดแกงเขียวหวาน", "303")
bowl4 = Bowl(150, "ข้าวไก่ทอด", "ไก่ทอดแกงเขียวหวาน", "304")
bowl5 = Bowl(150, "ข้าวไก่ทอด", "ไก่ทอดแกงเขียวหวาน", "305")
bowl6 = Bowl(120, "ข้าวไก่ทอด", "ไก่เผ็ด", "306")
bowl7 = Bowl(120, "ข้าวไก่ทอด", "ไก่เผ็ด", "307")
bowl8 = Bowl(120, "ข้าวไก่ทอด", "ไก่เผ็ด", "308")
bowl9 = Bowl(120, "ข้าวไก่ทอด", "ไก่เผ็ด", "309")
bowl10 = Bowl(120, "ข้าวไก่ทอด", "ไก่เผ็ด", "310")
bowl_recipe2=Bowl(80, "ข้าวเปล่า", None, None)
kfc_stock.add_recipe(bowl_recipe2)
bowl11 = Bowl(80, "ข้าวเปล่า", "-", "311")
bowl12 = Bowl(80, "ข้าวเปล่า", "-", "312")
bowl13 = Bowl(80, "ข้าวเปล่า", "-", "313")
bowl14 = Bowl(80, "ข้าวเปล่า", "-", "314")
bowl15 = Bowl(80, "ข้าวเปล่า", "-", "315")

kfc_stock.add_to_stock(bowl1)
kfc_stock.add_to_stock(bowl2)
kfc_stock.add_to_stock(bowl3)
kfc_stock.add_to_stock(bowl4)
kfc_stock.add_to_stock(bowl5)
kfc_stock.add_to_stock(bowl6)
kfc_stock.add_to_stock(bowl7)
kfc_stock.add_to_stock(bowl8)
kfc_stock.add_to_stock(bowl9)
kfc_stock.add_to_stock(bowl10)
kfc_stock.add_to_stock(bowl11)
kfc_stock.add_to_stock(bowl12)
kfc_stock.add_to_stock(bowl13)
kfc_stock.add_to_stock(bowl14)
kfc_stock.add_to_stock(bowl15)

### Boxset Instances
boxset_recipe1=Boxset("ชุดอิ่มคุ้ม", [chicken_recipe, drink_recipe2, snack_recipe1], 110, None)
kfc_stock.add_recipe(boxset_recipe1)
boxset1 = Boxset("ชุดอิ่มคุ้ม", [chicken1, drink9, chicken5], 110, "401")
boxset_recipe2=Boxset("ชุดอิ่มยันชาติหน้า", [bowl_recipe1, drink_recipe1, drink_recipe1], 250, None)
kfc_stock.add_recipe(boxset_recipe2)
boxset2 = Boxset("ชุดอิ่มยันชาติหน้า",[bowl2, drink2, snack2], 250 , "403")
boxset_recipe3=Boxset("ชุดคุ้มค่า", [chicken_recipe, drink_recipe1, snack_recipe1], 180, None)
kfc_stock.add_recipe(boxset_recipe3)
boxset3 = Boxset("ชุดคุ้มค่า", [chicken3, drink3, snack3], 180, "405" )

kfc_stock.add_to_stock(boxset1)
kfc_stock.add_to_stock(boxset2)
kfc_stock.add_to_stock(boxset3)

### Promotion Instances
promotion1 = Promotion("โปรอิ่มคุ้ม", [boxset1, boxset2,drink16], 400, "501")
promotion2 = Promotion("ลด 10%", [boxset2, boxset3], 320, "502")

promotion_recipe1=Promotion("โปรอิ่มคุ้ม", [boxset_recipe1, boxset_recipe2], 400, None)
promotion_recipe2=Promotion("ลด 10%", [boxset_recipe2, boxset_recipe3], 320, None)

kfc_stock.add_recipe(promotion_recipe1)
kfc_stock.add_recipe(promotion_recipe2)

kfc_stock.add_to_stock(promotion1)
kfc_stock.add_to_stock(promotion2)

### Coupon instance
coupon1 = Coupon("12345",0.15)
coupon2 = Coupon("54321",0.2)
coupon3 = Coupon("13579",0.25)

KFC1.add_coupon(coupon1)
KFC1.add_coupon(coupon2)
KFC1.add_coupon(coupon3)

KFC1.search_member_by_id("1").write_review(5,"อร่อยมากคับ")
KFC1.search_member_by_id("1").write_review(1,"อร่อยมากคับบบ")
KFC1.search_member_by_id("1").write_review(0,"อย่าหาซื้อ")
KFC1.search_member_by_id("1").write_review(0,"หนีไปมันคือกับดัก")
KFC1.search_member_by_id("1").write_review(0,"ผมสั่งไก่ทอด แต่ผมได้ทอดไก่")
KFC1.search_member_by_id("1").write_review(0,"ไก่ย่างวิเชียรอร่อยกว่าเยอะ ถูกกว่าด้วย")
KFC1.search_member_by_id("1").write_review(0,"อร่อยมากครับ ไก่ทอดเก4")

KFC1.search_member_by_id("1").add_address("home",["Thailand","Sakon Nakhon","Wanonniwas","Sriwichai","222","20","47120","home",None,None])
KFC1.search_member_by_id("1").add_address("office",["Thailand","Bangkok","Lard Krabang","Lard Krabang",None,"901","9999","home","ECC Build","หอพักนักศึกษา"])

###############################################################################################
################################-----API-----##################################################
###############################################################################################
    
app = FastAPI()
@app.get("/root")
def read_root():
    guest_id = Guest()
    KFC1.user_list.append(guest_id)
    user_dict = {}
    for user in KFC1.user_list:
        user_dict["id" + str(len(user_dict))] = user.id
    return {"Current" : guest_id.id, "all_user" : user_dict}

@app.get("/menu")
def open_menu():
    return KFC1.open_menu()

class dto_register(BaseModel):
    name:str
    username:str
    password:str
    guest_id:str

@app.post("/register")
def register(dto : dto_register):
    guest = KFC1.search_member_by_id(dto.guest_id)
    account=guest.register(dto.name, dto.username, dto.password)
    print(account)
    dictionary = {"name" : account.name, "id" : account.id}
    KFC1.user_list.remove(KFC1.search_member_by_id(dto.guest_id))
    return dictionary

class dto_login(BaseModel):
    username:str
    password:str
    guest_id:str

@app.post("/login")
def login(dto:dto_login):
    try:
        guest = KFC1.search_member_by_id(dto.guest_id)
        account = guest.login(dto.username,dto.password)
        print(account)
        dictionary = {"name" : account.name, "id" : account.id}
        KFC1.user_list.remove(KFC1.search_member_by_id(dto.guest_id))
        return dictionary
    except:
        return False


@app.get("/show_all_review")
def show_all_review():
    return KFC1.show_all_review()

class dto_show_transaction(BaseModel):
    id:str
    
@app.post("/show_transaction")
def show_transaction(dto : dto_show_transaction):  
    return  KFC1. show_transaction(dto.id)
        
class dto_show_address(BaseModel):
    id:str

@app.post("/show_address")
def show_address(dto:dto_show_address): 
    return KFC1.show_address(dto.id)

class dto_add_address(BaseModel):
    member_id:str
    address_name:str
    country:str
    city:str
    district:str
    subdistrict:str
    road:str
    house_number:str
    zip_code:str
    type:str
    landmark:str
    note:str

@app.post("/add_address")
def add_address(dto:dto_add_address):
    address_list = []
    address_list.append(dto.country)
    address_list.append(dto.city)
    address_list.append(dto.district)
    address_list.append(dto.subdistrict)
    address_list.append(dto.road)
    address_list.append(dto.house_number)
    address_list.append(dto.zip_code)
    address_list.append(dto.type)
    address_list.append(dto.landmark)
    address_list.append(dto.note)
    KFC1.search_member_by_id(dto.member_id).add_address(dto.address_name,address_list)
    return KFC1.show_address(dto.member_id)

class dto_delete_address(BaseModel):
    member_id:str
    address_name:str

@app.post("/remove_address")
def remove_address(dto:dto_delete_address):
    KFC1.search_member_by_id(dto.member_id).remove_address(dto.address_name)
    return KFC1.show_address(dto.member_id)

class dto_select_food(BaseModel):
    member_id: str
    meal_name: str
    
@app.post("/select_food")
def select_food(dto:dto_select_food):
    return KFC1.stock.select_food(dto.member_id,dto.meal_name)

class dto_modify_food(BaseModel):
    member_id: str
    meal_id: str
    attribute1: str
    attribute2: str

@app.post("/modify_food")
def modify_food(dto:dto_modify_food):
    KFC1.stock.modify_food(dto.member_id,dto.meal_id,dto.attribute1,dto.attribute2)
    return KFC1.search_member_by_id(dto.member_id).show_temp_selected()

class dto_show_summary(BaseModel):
    member_id: str

@app.post("/show_summary")
def show_summary(dto:dto_show_summary):
    return  KFC1.show_summary(dto.member_id)

class dto_add_to_cart(BaseModel):
    member_id:str

@app.post("/add_to_cart")
def add_to_cart(dto:dto_add_to_cart):
    KFC1.search_member_by_id(dto.member_id).add_to_cart()
    return KFC1.member_show_cart(dto.member_id)
    
class dto_show_cart(BaseModel):
    member_id:str

@app.post("/show_cart")
def member_show_cart(dto:dto_show_cart):
    return KFC1.member_show_cart(dto.member_id)

class dto_remove_item(BaseModel):
    member_id:str
    meal_id:str

@app.post("/remove_item")
def remove_item_from_cart(dto:dto_remove_item):
    KFC1.search_member_by_id(dto.member_id).remove_from_cart(dto.meal_id)
    return KFC1.member_show_cart(dto.member_id)

class dto_check_out(BaseModel):
    member_id:str

@app.post("/check_out")
def check_out(dto:dto_check_out):
    return KFC1.check_out(dto.member_id)

class dto_use_coupon(BaseModel):
    member_id:str
    coupon_code:str

@app.post("/use_coupon")
def use_coupon(dto:dto_use_coupon):
    return KFC1.use_coupon(dto.member_id,dto.coupon_code)

class dto_payment(BaseModel):
    member_id:str
    
@app.post("/payment")
def payment(dto:dto_payment):
    KFC1.search_member_by_id(dto.member_id).create_payment()
    return KFC1.show_payment(dto.member_id)

class dto_select_payment_method(BaseModel):
    member_id: str
    payment_method: str
    
@app.post("/select_payment_method")
def select_payment_method(dto : dto_select_payment_method):
    KFC1.search_member_by_id(dto.member_id).temp_payment.select_payment_method(dto.payment_method)
    return KFC1.show_payment(dto.member_id)

class dto_select_address(BaseModel):
    member_id: str
    address_name: str
    
@app.post("/select_address")
def select_address(dto : dto_select_address):
    KFC1.search_member_by_id(dto.member_id).temp_payment.select_address(dto.member_id,dto.address_name)
    return KFC1.show_payment(dto.member_id)

class dto_write_review(BaseModel):
    member_id: str
    score: int
    comment: str | None = None

@app.post("/write_review")
def write_review(dto : dto_write_review):
    KFC1.search_member_by_id(dto.member_id).write_review(dto.score,dto.comment)
    return KFC1.show_all_review()


class dto_success(BaseModel):
    member_id: str

@app.post("/payment_succsess")
def payment_success(dto:dto_success):
    return KFC1.search_member_by_id(dto.member_id).temp_payment.payment_success(KFC1.search_member_by_id(dto.member_id))

##################################################################################################################
###################################-Transaction-##################################################################
##################################################################################################################

#(self,id,item_list,date,price,used_coupon)

order1 = Order("1",[chicken10],"2021-08-12",150,"12345")
payment1 = Payment(order1)
payment1.select_payment_method("qr_code")
payment1.select_address("1","home")
KFC1.search_member_by_id("1").set_temp_payment(payment1)
print("temp payment1")
print(KFC1.search_member_by_id("1").temp_payment.order.item_list[0].id)
KFC1.search_member_by_id("1").temp_payment.payment_success(KFC1.search_member_by_id("1"))
print("seccess")
order2 = Order("2",[chicken15],"2021-08-12",300,None)
payment2 = Payment(order2)
payment2.select_payment_method("qr_code")
payment2.select_address("1","home")
KFC1.search_member_by_id("1").set_temp_payment(payment2)
print("temp payment2")
print(KFC1.search_member_by_id("1").temp_payment.order.item_list[0].id)
transaction_id = str(KFC1.search_member_by_id("1").id) + str(KFC1.search_member_by_id("1").temp_payment.order.order_id)
print(transaction_id)
KFC1.search_member_by_id("1").temp_payment.payment_success(KFC1.search_member_by_id("1"))
print(KFC1.search_member_by_id("1").show_my_transaction())
print(order1.order_id,order2.order_id)

##################################################################################################################
KFC1.search_member_by_id("1").set_temp_summary([chicken19])
KFC1.search_member_by_id("1").add_to_cart()
KFC1.search_member_by_id("1").set_temp_summary([drink16])
KFC1.search_member_by_id("1").add_to_cart()
print(KFC1.search_member_by_id("1").cart.meal_list)
KFC1.search_member_by_id("1").cart.check_out("1")
# for food in KFC1.stock.food_list:
#     print(food.id)