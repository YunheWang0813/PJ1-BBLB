from flask import request, redirect, url_for, render_template, flash
from bblb import app, db
from bblb.models import Menu
import random


@app.route('/')
def show_lootbox():
    return render_template('show_lootbox.html')


@app.route('/result', methods=['GET'])
def result():

    # params
    menus = []
    money = 10
    budget = money

    # select first coffee
    while not menus:
        rand = random.randrange(0, db.session.query(Menu.id).count()) + 1
        menus = db.session.query(Menu).filter(Menu.id == rand, Menu.price <= budget).all()

    # calculate
    budget -= float(menus[0].price)

    while budget > 0:

        # avalable food candidate
        candidate = db.session.query(Menu).filter(Menu.price <= budget).all()

        # no candidate break
        if not candidate:
            break

        # select coffee
        coffee = random.choice(candidate)

        # add to list
        menus.append(coffee)

        # calculate
        budget -= float(coffee.price)

    budget = money - budget

    return render_template('show_lootbox.html', menus=menus, budget=budget)
