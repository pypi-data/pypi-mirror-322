from PySide6 import QtCore
from beijing_fushengji.app.models import ItemName


class GameMessages(QtCore.QObject):
    def get(self):
        return self.messages

    def __init__(self, MainWidget):
        super().__init__()

        from dataclasses import dataclass

        @dataclass
        class GameMessage:
            freq: int
            msg: str
            drug: ItemName
            plus: int
            minus: int
            add: int

        gameMessages = [
            [
                170,
                MainWidget.tr(
                    'Experts propose to improve college students\' "hands-on quality", imported toys are popular!'
                ),
                ItemName.toys,
                2,
                0,
                0,
            ],
            [
                139,
                MainWidget.tr(
                    "Some people proudly say: When you are sick, you don't need to take injections or medicine, just drink fake liquor (very toxic)!"
                ),
                ItemName.liquor,
                3,
                0,
                0,
            ],
            [
                100,
                MainWidget.tr(
                    'Hospital\'s secret report: "Shanghai Baby" is more effective than Viagra"!'
                ),
                ItemName.r18_book,
                5,
                0,
                0,
            ],
            [
                41,
                MainWidget.tr(
                    'The illiterate said: "2000 Nobel Prize in Literature? Bah! Not as good as pirated VCD Hong Kong and Taiwan movies." ”'
                ),
                ItemName.vcd_game,
                4,
                0,
                0,
            ],
            [
                37,
                MainWidget.tr(
                    'Editorial of "Beijing Economic Newspaper": "Smuggling cars vigorously promotes car consumption!"'
                ),
                ItemName.car,
                3,
                0,
                0,
            ],
            [
                23,
                MainWidget.tr(
                    'Editorial of "Beijing Truth": "Promote beauty and put it into practice", counterfeit cosmetics are very popular!'
                ),
                ItemName.makeup,
                4,
                0,
                0,
            ],
            [
                37,
                MainWidget.tr(
                    '8858.com e-bookstore dare not sell "Shanghai Baby", a copy can be sold at a sky-high price on the black market!'
                ),
                ItemName.r18_book,
                8,
                0,
                0,
            ],
            [
                15,
                MainWidget.tr(
                    'Xie Bufeng said at the party: "I am cool! I use counterfeit cosmetics!", counterfeit cosmetics are in short supply!'
                ),
                ItemName.makeup,
                7,
                0,
                0,
            ],
            [
                40,
                MainWidget.tr(
                    "Some people in Beijing drink fake Shanxi wine crazily, and can sell it at a sky-high price!"
                ),
                ItemName.liquor,
                7,
                0,
                0,
            ],
            [
                29,
                MainWidget.tr(
                    "College students in Beijing start looking for jobs, parallel-imported mobile phones are very popular!!"
                ),
                ItemName.phone,
                7,
                0,
                0,
            ],
            [
                35,
                MainWidget.tr(
                    "Rich people in Beijing are crazy about buying smuggled cars! Prices are soaring!"
                ),
                ItemName.car,
                8,
                0,
                0,
            ],
            [
                17,
                MainWidget.tr(
                    "The market is flooded with smuggled cigarettes from Fujian!"
                ),
                ItemName.cigar,
                0,
                8,
                0,
            ],
            [
                24,
                MainWidget.tr(
                    "Children in Beijing are busy studying online, no one wants to buy imported toys."
                ),
                ItemName.toys,
                0,
                5,
                0,
            ],
            [
                18,
                MainWidget.tr(
                    'The piracy industry is booming, and Zhongguancun, the "Silicon Valley of China", is full of village girls selling pirated VCDs!'
                ),
                ItemName.vcd_game,
                0,
                8,
                0,
            ],
            [
                160,
                MainWidget.tr(
                    "My old classmate in Xiamen sponsored me two smuggled cars! I'm rich!"
                ),
                ItemName.car,
                0,
                0,
                2,
            ],
            [
                45,
                MainWidget.tr(
                    "After the Industrial and Commercial Bureau raided the place, I found the imported cigarettes lost by my fellow villager in a dark corner."
                ),
                ItemName.cigar,
                0,
                0,
                6,
            ],
            [
                35,
                MainWidget.tr(
                    "My fellow villager gave me some fake Shanxi liquor (highly toxic) before he went home!"
                ),
                ItemName.liquor,
                0,
                0,
                4,
            ],
            [
                140,
                MainWidget.tr(
                    "Media reports: Another Japanese product exported to China has gone wrong! After the incident, the Japanese refused to admit it and refused to compensate. The village chief learned of this news and asked someone to sell you his parallel-imported mobile phone (without any manufacturer logo) for 2,500 yuan."
                ),
                ItemName.phone,
                0,
                0,
                1,
            ],
        ]
        messages: list[GameMessage] = []
        for i in gameMessages:
            m = GameMessage(*i)
            # m.freq, m.msg, m.drug, m.plus, m.minus, m.add = i
            messages.append(m)

        self.messages = messages


class RandomEvents(QtCore.QObject):
    def get(self):
        return self.random_events

    def __init__(self):
        super().__init__()

        self.random_events = [
            [117, self.tr("Two hooligans beat me up on the street!"), 3, "kill.wav"],
            [
                157,
                self.tr("I was beaten up by a stick in the underpass!"),
                20,
                "death.wav",
            ],
            [
                21,
                self.tr(
                    "The Industrial and Commercial Bureau chased me through three alleys."
                ),
                1,
                "dog.wav",
            ],
            [
                100,
                self.tr("Beijing's congested traffic makes me anxious!"),
                1,
                "harley.wav",
            ],
            [35, self.tr("A minibus driver slapped me!"), 1, "hit.wav"],
            [313, self.tr("A group of migrant workers beat me up!"), 10, "flee.wav"],
            [
                120,
                self.tr("A young man in a nearby alley hit me with a brick!"),
                5,
                "death.wav",
            ],
            [
                29,
                self.tr(
                    "A fake security guard in a nearby office building shocked me with an electric baton!"
                ),
                3,
                "el.wav",
            ],
            [
                43,
                self.tr("The stinky black river in Beijing is making me sick!"),
                1,
                "vomit.wav",
            ],
            [
                45,
                self.tr(
                    "Auntie Wang, who is guarding bicycles, laughed at me for not having a Beijing hukou!"
                ),
                1,
                "level.wav",
            ],
            [
                48,
                self.tr("The temperature in Beijing is 40 degrees! I feel hot..."),
                1,
                "lan.wav",
            ],
            [
                33,
                self.tr(
                    "The Olympic bid has added a new landscape, and Beijing has another sandstorm!"
                ),
                1,
                "breath.wav",
            ],
        ]


class StealEvents(QtCore.QObject):
    def get(self):
        return self.events

    def __init__(self):
        super().__init__()

        self.events = [
            [
                60,
                self.tr(
                    "I feel sorry for the old lady pretending to be a beggar at the subway entrance."
                ),
                10,
            ],
            [
                125,
                self.tr(
                    'A man stopped me on the street and said, "Brother, give me some money!".'
                ),
                10,
            ],
            [100, self.tr('A big man touched me and said, "Stop squeezing!".'), 40],
            [
                65,
                self.tr(
                    'Three old ladies with red armbands grabbed me and said, "You are from another place? Fine!"'
                ),
                20,
            ],
            [
                35,
                self.tr(
                    'Two strong men grabbed me and said, "Pay the long-distance call surcharge and Internet fee."'
                ),
                15,
            ],
            [
                27,
                self.tr(
                    'The deputy director said, "Applying for a business license? Don\'t come to my house to give me money at night."'
                ),
                10,
            ],
            [
                40,
                self.tr(
                    "Beijing's air pollution is serious. I'm going to the oxygen bar to breathe oxygen..."
                ),
                5,
            ],
        ]
