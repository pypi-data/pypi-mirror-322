from PySide6 import QtWidgets, QtCore, QtMultimedia
import random
import os
import pickle
import base64

from beijing_fushengji.app.tools import load

from beijing_fushengji.app.models import Status
from beijing_fushengji.widgets.tables import BlackMarketTable, MyItemsTable
from beijing_fushengji.app.models import makeDrugPrices, get_item_name, Item, ItemName
from beijing_fushengji.app.events import RandomEvents, GameMessages, StealEvents
from beijing_fushengji.widgets.styled_widget import StyledWidget
from beijing_fushengji.widgets.styled_widget import StyledDialog


class MainWidget(StyledWidget):
    sig_time_pass = QtCore.Signal(int)
    sig_close = QtCore.Signal()

    def __init__(self):
        super().__init__()

        self.settings = QtCore.QSettings()

        self.ui = load("ui.main_widget").Ui_MainWidget()
        self.ui.setupUi(self)

        self.hide()

        self.d_story = load("widgets.story").StoryDlg()
        self.d_story.start_sig.connect(self.check_start)

        hide_intro = os.environ.get("HIDE_INTRO", False)
        if not hide_intro:
            self.show_intro()
        else:
            pass
        self.move(
            QtWidgets.QApplication.screens()[0].geometry().center()
            - self.rect().center()
        )
        self.n_cafe = 0
        self.ui.p_netcafe.clicked.connect(self.enter_cafe)
        self.ui.p_rent.clicked.connect(self.rent_house)

        self.ui.buy.clicked.connect(self.buy)
        self.ui.sell.clicked.connect(self.sell)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(20)
        self.timer.timeout.connect(self.scroll)
        self.t_pos = 0
        QtCore.QTimer.singleShot(7000, self.timer.start)
        self.ui.ticker.enterEvent = lambda _: self.timer.stop()
        self.ui.ticker.leaveEvent = lambda _: self.timer.start()

        self.places: list[QtWidgets.QPushButton] = [
            getattr(self.ui, f"x{i}") for i in range(10)
        ]
        for i in range(len(self.places)):
            self.places[i].clicked.connect(self.getaction(i))

        self.in_subway = True
        self.ui.switch_place.clicked.connect(self.switch_place)
        self.ui.switch_mode.clicked.connect(self.switch_mode)
        self.ui.p_bank.clicked.connect(self.enter_bank)
        self.ui.p_hospital.clicked.connect(self.enter_hospital)
        self.ui.p_postoffice.clicked.connect(self.pay_debt)

        self.init_data()
        self.refresh_display()
        self.indexes = []
        self.sell_indexes = []

    def black_market_items(self, selected, _deselected):
        if len(selected.indexes()) == 0:
            self.indexes = []
        else:
            self.indexes = [index.row() for index in selected.indexes()]

    def my_home_items(self, selected, _deselected):
        if len(selected.indexes()) == 0:
            self.sell_indexes = []
        else:
            self.sell_indexes = [index.row() for index in selected.indexes()]

    def pay_debt(self):
        if self.status.debt > 0:
            self.d_paydebt = load("widgets.pay_debt").PayDebt(
                self.status.cash, self.status.debt
            )
            self.d_paydebt.sig_pay.connect(self.after_pay_debt)
            self.d_paydebt.show()
        else:
            amount = self.status.cash + self.status.saving
            if amount < 1000:
                self.show_diary(
                    self.tr(
                        'The village chief laughed and said: "You have no money, you are crazy!"'
                    )
                )
            elif 1000 < amount < 100000:
                self.show_diary(
                    self.tr(
                        'The village chief nodded to me: "Brother, do you want to support your hometown with 1,000 yuan?"'
                    )
                )
            elif 100000 < amount < 10000000:
                self.show_diary(
                    self.tr(
                        'The village chief bowed to me on the phone: "Rich man! I want to marry my daughter to you."...'
                    )
                )
            elif amount > 10000000:
                self.show_diary(
                    self.tr(
                        'The village chief knelt down to me on the phone and said: "You are my real father!"'
                    )
                )
            else:
                self.show_diary(
                    self.tr(
                        'The village chief said: "You are a role model for rural young people!"'
                    )
                )

    def after_pay_debt(self, cash, debt):
        self.status.cash = cash
        self.status.debt = debt
        self.refresh_display()

    def show_diary(self, text: str):
        self.d_diary = load("widgets.simple_dialogs").Diary()
        self.d_diary.ui.label.setText(text)
        self.d_diary.exec()

    def show_news(self, text: str):
        self.d_diary = load("widgets.simple_dialogs").News()
        self.d_diary.ui.label.setText(text)
        self.d_diary.exec()

    def enter_hospital(self):
        import beijing_fushengji.widgets.hospital

        if self.status.health == 100:
            self.show_diary(
                self.tr(
                    'The young nurse looked at me with a smile and said, "Brother! Please register at the neurology department."'
                )
            )
        else:
            self.d_hospital = beijing_fushengji.widgets.hospital.Hospital(
                None, self.status.cash, self.status.health
            )
            self.d_hospital.sig_health.connect(self.leave_hospital)
            self.d_hospital.show()

    def leave_hospital(self, cash: int, health: int):
        self.status.cash = cash
        self.status.health = health
        self.refresh_display()

    def enter_bank(self):
        self.d_bank = load("widgets.bank").Bank(
            None, self.status.cash, self.status.saving
        )
        self.d_bank.sig_account.connect(self.leave_bank)
        self.d_bank.show()

    def leave_bank(self, cash, saving):
        self.status.cash = cash
        self.status.saving = saving
        self.refresh_display()

    def switch_mode(self):
        self.text_editor = load("widgets.simple_dialogs").TextEditor()
        self.text_editor.show()

    def switch_place(self):
        self.in_subway = not self.in_subway
        self.texts_subway = [
            self.tr("Beijing Railway \nStation"),
            self.tr("Pingguoyuan"),
            self.tr("Gongzhufen"),
            self.tr("Xizhimen"),
            self.tr("Jishuitan"),
            self.tr("Dongzhimen"),
            self.tr("Fuxingmen"),
            self.tr("Jianguomen"),
            self.tr("Changchun Street"),
            self.tr("Chongwenmen"),
        ]
        self.texts_city = [
            self.tr("Fangzhuang"),
            self.tr("Bajiao West Road"),
            self.tr("Cuiwei Road"),
            self.tr("Haidian Street"),
            self.tr("Asian Games Village"),
            self.tr("Sanyuan West Bridge"),
            self.tr("Fuyou Street"),
            self.tr("Yong'anli"),
            self.tr("Yuquanying"),
            self.tr("Yongdingmen"),
        ]
        for i in self.places:
            i.setDisabled(False)
        if self.in_subway:
            self.ui.switch_place.setText(self.tr("I want to visit \nthe capital"))
            for i in range(len(self.places)):
                self.places[i].setText(self.texts_subway[i])
        else:
            self.ui.switch_place.setText(self.tr("I want to go\n to the subway"))
            for i in range(len(self.places)):
                self.places[i].setText(self.texts_city[i])

    def getaction(self, btn_number: int):
        def action():
            for i in self.places:
                i.setDisabled(False)
            self.places[btn_number].setDisabled(True)
            self.handle_normal_events()

        return action

    def rent_house(self):
        if self.max_quantity == 140:
            self.show_diary(
                self.tr(
                    "The agent said, your house is bigger than the director's! And you're still renting?"
                )
            )
            return

        if self.status.cash < 30000:
            self.show_diary(
                self.tr(
                    "The agent said, you don't have 30,000 cash and you want to rent? Go away!"
                )
            )
        else:
            self.d_rent = load("widgets.simple_dialogs").Rent(
                self.status.cash, self.max_quantity
            )
            ret = self.d_rent.exec()
            if ret == StyledDialog.Accepted:
                self.status.cash = int(self.status.cash) / 2
                self.status.cash -= 2000
                self.max_quantity += 10
                self.refresh_display()

                self.show_diary(
                    self.tr(
                        "My house can hold {} items! But it seems that the agency cheated me of some money..."
                    ).format(self.max_quantity)
                )
            else:
                self.show_diary(
                    self.tr(
                        "Ha! Be careful! Rumor has it that some rental agencies in Beijing are very good at cheating people..."
                    )
                )

    def show_settings(self):
        self.d_settings = load("widgets.simple_dialogs").Settings(
            None, self.allow_hacker, self.turn_off_sound
        )
        self.d_settings.show()
        self.d_settings.sig_settings.connect(self.d_settings)

    def go_airport(self):
        self.play_sound("airport.wav")
        self.d_airport = load("widgets.simple_dialogs").Airport()
        self.d_airport.show()

    def show_about(self):
        self.about_game = load("widgets.about").AboutGame()
        self.about_game.show()

    def d_settings(self, allow_hacker: bool, turn_off_sound: bool):
        self.turn_off_sound = turn_off_sound
        if turn_off_sound:
            self.settings.setValue("no_sound", "true")
        else:
            self.settings.setValue("no_sound", "false")
        self.allow_hacker = allow_hacker
        if allow_hacker:
            self.settings.setValue("allow_hacker", "true")
        else:
            self.settings.setValue("allow_hacker", "false")

    def init_data(self, reset=False):
        self.bad_fame1_shown = False
        self.bad_fame2_shown = False
        self.turn_off_sound = self.settings.value("no_sound", "false") == "false"

        if os.environ.get("NOSOUND"):
            self.turn_off_sound = True
        self.allow_hacker = self.settings.value("allow_hacker", "false") == "false"

        if reset:
            self.quantity = 0
            self.max_quantity = 100
            self.status, _market_items, self.my_items = Status(), [], []
            self.market_items: list[Item] = makeDrugPrices(3)
            self.time_left = 40
        else:
            self.quantity = self.settings.value("quantity", 0)
            self.max_quantity = self.settings.value("max_quantity", 100)
            self.status, self.market_items, self.my_items = self.load_data()
            self.time_left = self.settings.value("time_left", 40)

        self.t_1 = BlackMarketTable(self.ui.black_market)
        self.t_2 = MyItemsTable(self.ui.my_room)

        self.ui.black_market.selectionModel().selectionChanged.connect(
            self.black_market_items
        )
        self.ui.my_room.selectionModel().selectionChanged.connect(self.my_home_items)

        self.quantity = sum(x.quantity for x in self.my_items)

        self.sig_time_pass.emit(self.time_left)

    def load_data(self) -> (Status, list[Item], list[Item]):
        status = Status()
        market_items = makeDrugPrices(3)
        my_items = []

        default = [status, market_items, my_items]
        val = pickle.dumps(default)
        default_obj = base64.b64encode(val).decode()

        obj = self.settings.value("status", default_obj)
        return pickle.loads(base64.b64decode(obj))

    def save(self):
        data = [self.status, self.market_items, self.my_items]
        val = pickle.dumps(data)
        obj = base64.b64encode(val).decode()
        self.settings.setValue("status", obj)
        self.settings.setValue("quantity", self.quantity)
        self.settings.setValue("max_quantity", self.max_quantity)
        self.settings.setValue("time_left", self.time_left)

    def handle_cash_and_debt(self):
        self.status.debt *= 1.1
        self.status.saving *= 1.01

        self.status.debt = int(self.status.debt)
        self.status.saving = int(self.status.saving)

    def decrease_time(self, _days: int = 1):
        self.time_left -= 1
        self.sig_time_pass.emit(self.time_left)

    def handle_normal_events(self):
        if self.time_left <= 2:
            self.market_items = makeDrugPrices(0)
        else:
            self.market_items = makeDrugPrices(3)
        self.handle_cash_and_debt()
        self.do_random_stuff()
        self.do_random_event()
        self.on_steal()

        if self.status.debt > 100000:
            self.show_diary(
                self.tr(
                    "I owed too much money, so the village chief called a group of villagers to beat me up!"
                )
            )
            self.play_sound("kill.wav")
            self.status.health -= 30
            self.refresh_display()

        self.decrease_time()

        if self.time_left == 1:
            self.show_diary(
                self.tr(
                    "I'm going back to my hometown tomorrow and selling all the goods quickly."
                )
            )
        if self.time_left == 0:
            self.show_diary(
                self.tr(
                    "I have been in Beijing for 40 days, it’s time to go back and get married."
                )
            )
            if len(self.my_items) != 0:
                self.show_diary(
                    self.tr("The system sold the remaining goods for me: {}").format(
                        ",".join(list(map(get_item_name, self.my_items)))
                    )
                )
                for i in self.my_items:
                    self.status.cash += self.get_price(i) * i.quantity
                self.my_items = []
            self.on_exit()

        self.refresh_display()

    def do_random_event(self):
        self.random_events = RandomEvents().get()
        for i in self.random_events:
            r = random.randint(0, 1000 - 1)
            if r % i[0] == 0:
                self.show_diary(
                    i[1] + self.tr(" My health decreases {} point.").format(i[2])
                )
                self.play_sound(i[3])
                self.status.health -= i[2]
                self.refresh_display()

        msg = self.tr(
            "Because I didn't take care of myself, I was found unconscious next to {} near {}."
        )
        msg2 = self.tr(
            "Kind citizens carried me to the hospital, and the doctor told me to be treated for {} days."
        )
        msg3 = self.tr(
            "The village chief asked someone to advance {} yuan for my hospitalization fee."
        )
        msg4 = self.tr("My health... health crisis... go to the doctor...")
        msg5 = self.tr(
            'I fell on the street, and the diary beside me said: "Beijing, I will come again!"'
        )

        self.down_places = [
            self.tr("In the hair salon"),
            self.tr("at the breakfast stall"),
            self.tr("at the newsstand"),
            self.tr("at the roast lamb stall"),
            self.tr("in the bus"),
            self.tr("on the rickshaw"),
            self.tr("in the women's restroom"),
            self.tr("in the men's restroom"),
            self.tr("in the telephone booth"),
            self.tr("in the arms of the escort girl"),
            self.tr("in the taxi"),
            self.tr("in the minibus"),
            self.tr("in the beauty salon"),
            self.tr("in the small kiosk"),
            self.tr("in front of the small shopping mall"),
            self.tr("at the feet of the migrant workers"),
            self.tr("in the stalls of unlicensed peddlers"),
            self.tr("on the grass"),
            self.tr("on the top of the telephone pole"),
            self.tr("in the small restaurant"),
            self.tr("on the side of the road"),
            self.tr("on the sidewalk"),
            self.tr("in the central park"),
            self.tr("under the billboard"),
            self.tr("in the bus station"),
            self.tr("in the long-distance bus station"),
            self.tr("next to the pirated game seller"),
            self.tr("next to the corpse of a Internet company"),
            self.tr("next to the fraudulent intellectual property owner"),
        ]

        if self.status.health < 85 and self.time_left > 3:
            delay_day = 1 + random.randint(0, 1)
            place = ""
            for i in self.places:
                if not i.isEnabled():
                    place = i.text()
            place2 = self.down_places[random.randint(0, len(self.down_places) - 1)]
            messages = []
            messages.append(msg.format(place, place2))
            messages.append(msg2.format(delay_day))

            load = 1000 + random.randint(0, 8500)
            messages.append(msg3.format(load))

            self.show_diary("\n".join(messages))

            self.status.debt += load
            self.status.health += 10
            self.time_left -= delay_day

        if 20 > self.status.health > 0:
            self.show_diary(msg4)
        if self.status.health < 0:
            self.play_sound("death.wav")
            self.show_diary(msg5)
            self.on_exit()

        self.refresh_display()

    def do_random_stuff(self):
        messages = GameMessages(self).get()

        for k, message in enumerate(messages):
            r = random.randint(0, 950)

            if r % message.freq == 0:
                if message.drug not in [x.name for x in self.market_items]:
                    continue
                index = [x.name for x in self.market_items].index(message.drug)

                self.show_news(message.msg)
                if k == len(messages) - 1:
                    self.status.debt += 2500

                # price multipled
                if message.plus > 0:
                    self.market_items[index].price *= message.plus
                # price divided
                if message.minus > 0:
                    self.market_items[index].price /= message.minus
                    self.market_items[index].price = int(self.market_items[index].price)

                if message.add > 0:
                    max_add_count = self.max_quantity - self.quantity
                    add_count = min(message.add, max_add_count)
                    if add_count == 0:
                        self.show_diary(
                            self.tr(
                                "What a pity! The house I rented is too small and can only hold {} items."
                            ).format(self.max_quantity)
                        )
                    else:
                        item = Item()
                        item.name = message.drug
                        item.price = 0
                        item.quantity = add_count
                        if k == len(messages) - 1:
                            item.price = 2500

                        if item.name not in [x.name for x in self.my_items]:
                            self.my_items.append(item)
                        else:
                            index = [x.name for x in self.my_items].index(item.name)
                            self.my_items[index].quantity += add_count

        self.refresh_display()

    def on_steal(self):
        self.steal_events = StealEvents().get()
        self.hacker_msg = self.tr(
            "Hackers hacked into the bank network and frantically modified the database. My deposit decreased by {}"
        )
        self.hacker_msg2 = self.tr(
            "Hackers hacked into the bank network and frantically modified the database. My deposit increased by {}"
        )

        self.msg2 = self.tr("I am in trouble.")

        self.msg3 = self.tr("My money decreased by {} percent.")
        self.msg_4 = self.tr("My deposit decreased by {} percent. Oh no!")

        for i, event in enumerate(self.steal_events):
            if random.randint(0, 999) % event[0] == 0:
                if i not in (4, 5):
                    msg = event[1] + self.msg3.format(event[2])
                    self.show_diary(msg)
                    self.status.cash *= 1 - event[2] / 100
                    self.status.cash = int(self.status.cash)
                else:
                    if self.status.saving > 0:
                        msg = event[1] + self.msg_4.format(event[2])
                        self.show_diary(msg)
                        self.status.saving *= 1 - event[2] / 100
                        self.status.saving = int(self.status.saving)

        if random.randint(0, 999) % 25 == 0 and self.allow_hacker:
            if self.status.saving < 1000:
                pass
            else:
                if self.status.saving > 100000:
                    num = int(self.status.saving / (2 + random.randint(0, 19)))
                    if random.randint(0, 19) % 3 == 0:
                        self.status.saving -= num
                        self.show_diary(self.hacker_msg.format(num))
                    else:
                        self.status.saving += num
                        self.show_diary(self.hacker_msg2.format(num))
                else:
                    num = int(self.status.saving / (1 + random.randint(0, 14)))
                    self.status.saving += num
                    self.show_diary(self.hacker_msg2.format(num))

        if self.status.cash < 0:
            self.status.cash = 0
            self.show_diary(self.msg2)

        self.refresh_display()

    def show_top_players(self):
        self.top_players = load("widgets.top_players").TopPlayers()
        self.top_players.exec()

    def on_exit(self):
        self.top_players = load("widgets.top_players").TopPlayers()
        score = self.status.cash + self.status.saving - self.status.debt
        if score > 0:
            i = self.top_players.get_my_order(score)
            if i != 100:
                self.d_celebrate = load("widgets.simple_dialogs").CelebrateWindow(
                    score, i
                )
                self.d_celebrate.exec()
                self.top_players.insert_score(
                    self.d_celebrate.get_name(),
                    score,
                    self.status.health,
                    self.status.fame,
                )
            else:
                self.show_news(
                    self.tr(
                        "The {} money you earned is too little, so you failed to enter the top 10 rich people. Try harder next time!"
                    ).format(score)
                )

            self.top_players.exec()

            if score > 10000000:
                self.show_news(
                    self.tr(
                        "The money you earned, {} RMB, is very high. It is recommended that you send it to the author for expert ranking."
                    )
                )
        else:
            self.show_news(
                self.tr(
                    'The Beijing Game News reported: Player "Anonymous" failed to make money in Beijing and was sent home.'
                )
            )

        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle("Confirmation")
        msg_box.setText(self.tr("Hey, wanna play again?"))
        msg_box.setStandardButtons(
            QtWidgets.QMessageBox.StandardButton.Yes
            | QtWidgets.QMessageBox.StandardButton.No
        )
        msg_box.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)

        result = msg_box.exec()

        if result == QtWidgets.QMessageBox.StandardButton.Yes:
            self.time_left = 40  # avoid bug for new_game dialog
            self.on_new_game()
        else:
            self.remove_help_file()
            self.sig_close.emit()
            self.close()

    def remove_help_file(self):
        self.d_story.remove_help_file()

    def on_new_game(self):
        if 40 - self.time_left >= 3:
            msg_box = QtWidgets.QMessageBox()
            msg_box.setWindowTitle("Confirmation")
            msg_box.setText(
                self.tr(
                    "Do you want abandon currently-playing game and start a new one?"
                )
            )
            msg_box.setStandardButtons(
                QtWidgets.QMessageBox.StandardButton.Yes
                | QtWidgets.QMessageBox.StandardButton.No
            )
            msg_box.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)

            result = msg_box.exec()

            if result == QtWidgets.QMessageBox.StandardButton.No:
                return

        self.init_data(reset=True)
        self.refresh_display()
        self.indexes = []
        self.sell_indexes = []
        self.show()

    def play_sound(self, name: str):
        if not self.turn_off_sound:
            # the "self" is important because sound will run in the background
            self.effect = QtMultimedia.QSoundEffect()
            self.effect.setSource(QtCore.QUrl.fromLocalFile(f":/SND/sound/{name}"))
            self.effect.setLoopCount(1)
            self.effect.setVolume(0.8)
            self.effect.play()

    def buy(self):
        if len(self.indexes) == 0:
            self.show_diary(self.tr("I haven't decided what to buy yet."))
        else:
            item = self.market_items[self.indexes[0]]
            if self.status.cash < item.price:
                if self.status.saving > 0:
                    self.show_diary(
                        self.tr(
                            "I don't have enough cash with me, so I'll go to the bank to withdraw some money."
                        )
                    )
                else:
                    self.show_diary(
                        self.tr(
                            "I don't have enough cash and I don't have any deposits in the bank, what should I do?"
                        )
                    )
            else:
                self.d_buy = load("widgets.buy").Buy(
                    self.status.cash,
                    self.market_items[self.indexes[0]],
                    self.quantity,
                    self.max_quantity,
                )
                self.d_buy.ui.pushButton.clicked.connect(self.finish_buy)
                self.d_buy.show()

    def finish_buy(self):
        buy_amount = self.d_buy.ui.spinBox.value()
        if buy_amount != 0:
            self.play_sound("buy.wav")
            self.status.cash -= self.d_buy.item.price * buy_amount
            item = self.d_buy.item
            item.quantity = buy_amount
            self.my_items.append(item)
            self.refresh_display()

    def sell(self):
        if len(self.sell_indexes) == 0:
            pass
        else:
            item = self.my_items[self.sell_indexes[0]]

            price = self.get_price(item)
            if price == -1:
                self.show_diary(
                    self.tr(
                        "Oh? It seems that no one is doing {} business here."
                    ).format(get_item_name(item))
                )
            else:
                self.d_sell = load("widgets.simple_dialogs").Sell(item)
                self.d_sell.ui.pushButton.clicked.connect(self.finish_sell)
                self.d_sell.show()

    def get_price(self, item: Item):
        names = [x.name for x in self.market_items]
        if item.name in names:
            index = names.index(item.name)
            market_item = self.market_items[index]
            return market_item.price
        return -1

    def finish_sell(self):
        self.play_sound("money.wav")
        quantity = self.d_sell.ui.spinBox.value()
        self.status.cash += quantity * self.get_price(self.d_sell.item)
        names = [x.name for x in self.my_items]
        index = names.index(self.d_sell.item.name)
        self.my_items[index].quantity -= quantity
        if self.my_items[index].quantity == 0:
            del self.my_items[index]

        item = self.d_sell.item
        if item.name == ItemName.r18_book:
            self.status.fame -= 7
            if not self.bad_fame1_shown:
                self.bad_fame1_shown = True
                self.show_diary(
                    self.tr(
                        'Buying and selling "Shanghai Baby" (banned book) pollutes society and my reputation has become bad!'
                    )
                )
        elif item.name == ItemName.liquor:
            self.status.fame -= 10
            if not self.bad_fame2_shown:
                self.bad_fame2_shown = True
                self.show_diary(
                    self.tr(
                        "Buying and selling fake liquor (very poisonous!) harms society and my reputation has declined."
                    )
                )
        self.refresh_display()

    def scroll(self):
        self.t_pos += 1.1
        bar = self.ui.ticker.horizontalScrollBar()
        bar.setValue(int(self.t_pos))
        if self.t_pos > bar.maximum():
            self.timer.stop()
            self.timer_restart = QtCore.QTimer()
            self.timer_restart.timeout.connect(self.restart_scroll)
            self.timer_restart.setSingleShot(True)
            self.timer_restart.start(60 * 1000)

    def restart_scroll(self):
        self.t_pos = 0
        QtCore.QTimer.singleShot(7000, self.timer.start)

    def enter_cafe(self):
        if self.status.cash < 15:
            self.show_diary(
                self.tr(
                    "You need to bring at least 15 yuan with you when entering an Internet cafe, haha, come back after withdrawing money."
                )
            )
        elif self.n_cafe > 2:
            self.show_diary(
                self.tr(
                    "The village chief said: Don't hang out in the Internet cafe all the time, go and do a decent business!"
                )
            )
        else:
            self.n_cafe += 1
            self.cafe = load("widgets.simple_dialogs").CyberCafe()
            self.cafe.ui.leave_cybercafe.clicked.connect(self.finish_cyber_cafe)
            self.cafe.show()

    def finish_cyber_cafe(self):
        money = random.randint(1, 10)
        self.status.cash += money
        self.refresh_display()

        self.show_diary(
            self.tr(
                "Thanks to the telecommunications reform, you can surf the Internet for free! And I also earned {} yuan in US Internet advertising fees, hehe!"
            ).format(money)
        )

    def refresh_display(self):
        self.ui.cash.display(self.status.cash)
        self.ui.saving.display(self.status.saving)
        if self.status.fame < 60:
            self.status.fame = max(self.status.fame, 0)
            self.ui.fame.setStyleSheet("color: rgb(240, 0, 0);")
        self.ui.fame.display(self.status.fame)
        self.ui.debt.display(self.status.debt)
        self.ui.health.display(self.status.health)

        self.t_1.slot_items(self.market_items)
        self.t_2.slot_items(self.my_items)

        self.quantity = sum(x.quantity for x in self.my_items)
        self.ui.label_7.setText(
            self.tr("your rented house ({}/{})").format(
                self.quantity, self.max_quantity
            )
        )

    def show_intro(self):
        self.d_story.exec()

    def check_start(self):
        self.show()
