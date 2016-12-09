# -*- coding: utf-8 -*-
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Categories, Books, Users, CheckOut, CheckIn
engine = create_engine('sqlite:///librarydata.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
sess = DBSession()

# Clear existing database
sess.query(Categories).delete()
sess.commit()
sess.query(Books).delete()
sess.commit()
print "All Categories and Books cleared"
sess.query(Users).delete()
sess.commit()
print "All Users cleared"
sess.query(CheckOut).delete()
sess.commit()
print "All Checked out Records cleared"
sess.query(CheckIn).delete()
sess.commit()
print "All Checked in Records cleared"

# Create dummy Users and an Admin
Admin1 = Users(
    name = "John Doe",
    email = "john@doe.com",
    administrator = True)

sess.add(Admin1)
sess.commit()

User1 = Users(
    name = "Steve Jobs",
    email = "steve@jobs.com",
    administrator = False)

sess.add(User1)
sess.commit()

User2 = Users(
    name = "Tim Cook",
    email = "tim@cook.com",
    administrator = False)

sess.add(User2)
sess.commit()

User3 = Users(
    name = "Jonny Ive",
    email = "jonny@ive.com",
    administrator = False)

sess.add(User3)
sess.commit()

users = sess.query(Users).all()
print "The following users were added:"
for u in users:
    print u.name, u.id

# Create Categories

cat1 = Categories(
    name = "Fiction",
    user_id = 1)
sess.add(cat1)
sess.commit()

cat2 = Categories(
    name = "Cookbooks",
    user_id = 1)
sess.add(cat2)
sess.commit()

cat3 = Categories(
    name = "Biographies",
    user_id = 1)
sess.add(cat3)
sess.commit()

cat4 = Categories(
    name = "Sports",
    user_id = 1)
sess.add(cat4)
sess.commit()

cat5 = Categories(
    name = "History",
    user_id = 1)
sess.add(cat5)
sess.commit()


cat7 = Categories(
    name = "Kids",
    user_id = 1)
sess.add(cat7)
sess.commit()



cats = sess.query(Categories).all()
print "The following categories were added:"
for c in cats:
    print c.name

# Create Books
ruser = random.randrange(1, 4)

book1 = Books(
    title = "Take Heart, My Child: A Mother's Dream",
    image = "https://images-na.ssl-images-amazon.com/images/I/515MrbUcuwL.jpg",
    description = u'''In the tradition of Emily Winfield Martin’s The Wonderful Things You Will Be and Nancy Tillman’s On The Night You Were Born, popular FOX news anchor Ainsley Earhardt’s lyrical lullaby inspires children to follow their dreams and passions.

    FOX and Friends cohost Ainsley Earhardt’s debut picture book shares precious life lessons parents can pass onto their children so that they can follow their hearts, dreams, and passions.

    Take Heart, My Child is a lyrical lullaby, and Ainsley shares her own hopes and dreams, and lets her child know that whatever challenges life brings, “Take heart, my child, I will—or, my love will—always be there for you.” It’s a universal message, one that all readers will relate to.

    In the “Story Behind the Story,” Ainsley talks about growing up and how her father would write messages to her and her siblings each morning, leaving notes at the breakfast table, so that his children would know they were loved, empowered, protected, and cherished.',
    ''',
    author = "Ainsley Earhardt",
    isbn = "481466224",
    category = 6,
    user_id = ruser,
    )
sess.add(book1)
sess.commit()

book2 = Books(
    title = "Give Please a Chance",
    image = "https://images-na.ssl-images-amazon.com/images/I/51fflhavjTL.jpg",
    description = u'''In this instant classic, Bill O'Reilly and James Patterson together present a beautifully illustrated picture book that celebrates the magic of the word "Please" for our children.

    In this inspired collaboration, bestselling authors Bill O'Reilly and James Patterson remind us all that a single word--"Please?"--is useful in a thousand different ways. From finding a lovable stray dog to needing a partner on a seesaw, from reading a bedtime story to really, really needing a cookie, Give Please a Chance depicts scenes and situations in which one small word can move mountains.

    With a vivid array of illustrations by seventeen different artists, this charming, helpful book is a fun and memorable way for children to learn the magic power of one simple word: please.
    ''',
    author = "Bill O'Reilly",
    isbn = "031627688X",
    category = 6,
    user_id = ruser,
    )
sess.add(book2)
sess.commit()

book2 = Books(
    title = "Our Revolution: A Future to Believe In",
    image = "https://images-na.ssl-images-amazon.com/images/I/51KL-VWz5rL.jpg",
    description = u'''When Bernie Sanders began his race for the presidency, it was considered by the political establishment and the media to be a “fringe” campaign, something not to be taken seriously. After all, he was just an independent senator from a small state with little name recognition. His campaign had no money, no political organization, and it was taking on the entire Democratic Party establishment.

    By the time Sanders’s campaign came to a close, however, it was clear that the pundits had gotten it wrong. Bernie had run one of the most consequential campaigns in the modern history of the country. He had received more than 13 million votes in primaries and caucuses throughout the country, won twenty-two states, and more than 1.4 million people had attended his public meetings. Most important, he showed that the American people were prepared to take on the greed and irresponsibility of corporate America and the 1 percent.

    In Our Revolution, Sanders shares his personal experiences from the campaign trail, recounting the details of his historic primary fight and the people who made it possible. And for the millions looking to continue the political revolution, he outlines a progressive economic, environmental, racial, and social justice agenda that will create jobs, raise wages, protect the environment, and provide health care for all―and ultimately transform our country and our world for the better. For him, the political revolution has just started. The campaign may be over, but the struggle goes on.
    ''',
    author = "Bernie Sanders",
    isbn = "1250132924",
    category = 3,
    user_id = ruser,
    )
sess.add(book2)
sess.commit()

book2 = Books(
    title = "Diary of a Wimpy Kid # 11: Double Down",
    image = "https://images-na.ssl-images-amazon.com/images/I/51qwnfm6EhL.jpg",
    description = u'''The pressure’s really piling up on Greg Heffley. His mom thinks video games are turning his brain to mush, so she wants her son to put down the controller and explore his “creative side.”

    As if that’s not scary enough, Halloween’s just around the corner and the frights are coming at Greg from every angle.

    When Greg discovers a bag of gummy worms, it sparks an idea. Can he get his mom off his back by making a movie . . . and will he become rich and famous in the process? Or will doubling down on this plan just double Greg’s troubles?
    ''',
    author = "Jeff Kinney",
    isbn = "1250132924",
    category = 1,
    user_id = ruser,
    )
sess.add(book2)
sess.commit()

book2 = Books(
    title = "Cooking for Jeffrey: A Barefoot Contessa Cookbook",
    image = "https://images-na.ssl-images-amazon.com/images/I/51Gp4L5L9YL.jpg",
    description = u'''For America’s bestselling cookbook author Ina Garten there is no greater pleasure than cooking for the people she loves—and particularly for her husband, Jeffrey. She has been cooking for him ever since they were married forty-eight years ago, and the comforting, delicious meals they shared became the basis for her extraordinary career in food.

    Ina’s most personal cookbook yet, Cooking for Jeffrey is filled with the recipes Jeffrey and their friends request most often as well as charming stories from Ina and Jeffrey’s many years together. There are traditional dishes that she’s updated, such as Brisket with Onions and Leeks, and Tsimmes, a vegetable stew with carrots, butternut squash, sweet potatoes, and prunes, and new favorites, like Skillet-Roasted Lemon Chicken and Roasted Salmon Tacos. You’ll also find wonderful new salads, including Maple-Roasted Carrot Salad and Kale Salad with Pancetta and Pecorino. Desserts range from simple Apple Pie Bars to showstoppers like Vanilla Rum Panna Cotta with Salted Caramel. For the first time, Ina has included a chapter devoted to bread and cheese, with recipes and tips for creating the perfect cheese course. With options like Fig and Goat Cheese Bruschettas and Challah with Saffron, there’s something everyone will enjoy.

    From satisfying lunches to elegant dinners, here are the recipes Ina has tested over and over again, so you too can serve them with confidence to the people you love.
    ''',
    author = "Ina Garten",
    isbn = "030746489X",
    category = 2,
    user_id = ruser,
    )
sess.add(book2)
sess.commit()

book2 = Books(
    title = "Green Smoothies for Life",
    image = "https://images-na.ssl-images-amazon.com/images/I/51tqNzVzZkL.jpg",
    description = u'''A brand-new meal plan that will assist readers with incorporating green smoothies into their everyday routine while developing healthier long-term eating habits and improving their overall health.

    More than a weight loss plan, the 10-Day Green Smoothie Cleanse, designed by nutritionist and certified weight-loss expert JJ Smith, became a way of life. Readers reported that they not only shed pounds but they also slept better, thought more clearly, and were in better over-all health, with some adherents, in consultation with their doctor, even moving off medication. As delicious as her green smoothies are, however, the cleanse was designed only to jumpstart a detox and a new approach to eating—it’s not a permanent solution.

    In her new book, Green Smoothies for Life, the highly anticipated follow up to the #1 New York Times bestseller 10-Day Green Smoothie Cleanse, Smith presents a way that green smoothies can be incorporated into your daily regimen. With over thirty recipes for everything from hot dinners to desserts and snacks, sixty thoughtfully composed green smoothie recipes, a thirty-day meal plan and the corresponding shopping lists, the book provides you with a step-by-step prescriptive daily regimen that shows you how to eat mindfully and healthily. In addition to green smoothies and color photographs of select recipes, the book includes more than twenty effective methods to detox (which helps fuel weight loss), information on Smith’s DHEMM (Detox, Hormonal Balance, Eat, Move and Mental Mastery) weight loss system, and testimonials from dieters who’ve change their approach to not just food but also life since while following her advice.

    Whether you are just starting out on your weight loss journey or already a smoothie convert, Green Smoothies for Life is the essential next step in continuing your pursuit of a healthier lifestyle.
    ''',
    author = "JJ Smith",
    isbn = "1501100653",
    category = 2,
    user_id = ruser,
    )
sess.add(book2)
sess.commit()

book2 = Books(
    title = "Harry Potter and the Sorcerer's Stone",
    image = "https://images-na.ssl-images-amazon.com/images/I/51NyRnx-FOL.jpg",
    description = u'''"Turning the envelope over, his hand trembling, Harry saw a purple wax seal bearing a coat of arms; a lion, an eagle, a badger and a snake surrounding a large letter 'H'."

    Harry Potter has never even heard of Hogwarts when the letters start dropping on the doormat at number four, Privet Drive. Addressed in green ink on yellowish parchment with a purple seal, they are swiftly confiscated by his grisly aunt and uncle. Then, on Harry's eleventh birthday, a great beetle-eyed giant of a man called Rubeus Hagrid bursts in with some astonishing news: Harry Potter is a wizard, and he has a place at Hogwarts School of Witchcraft and Wizardry. An incredible adventure is about to begin!
    ''',
    author = "JK Rowling",
    isbn = "0439708184",
    category = 1,
    user_id = ruser,
    )
sess.add(book2)
sess.commit()

book2 = Books(
    title = "Ocean of Storms",
    image = "https://images-na.ssl-images-amazon.com/images/I/51yy3YAdMEL.jpg",
    description = u'''"In the near future, political tensions between the United States and China are at an all-time high. Then a catastrophic explosion on the moon cleaves a vast gash in the lunar surface, and the massive electromagnetic pulse it unleashes obliterates Earth’s electrical infrastructure. To plumb the depths of the newly created lunar fissure and excavate the source of the power surge, the feuding nations are forced to cooperate on a high-risk mission to return mankind to the moon.

    Now, a diverse, highly skilled ensemble of astronauts—and a pair of maverick archaeologists plucked from the Peruvian jungle—will brave conspiracy on Earth and disaster in space to make a shocking discovery.

    Ocean of Storms is an epic adventure that spans space and time as its heroes race to fulfill an ancient mission that may change the course of humanity’s future.
    ''',
    author = "Christopher Mari",
    isbn = "B01CQF27N4",
    category = 1,
    user_id = ruser,
    )
sess.add(book2)
sess.commit()

book2 = Books(
    title = "The Atlantis Gene: A Thriller",
    image = "https://images-na.ssl-images-amazon.com/images/I/51sLuf5ZJmL.jpg",
    description = u'''"Read the novel that started it all. The Atlantis Gene is the first book in The Origin Mystery, the global bestselling trilogy that is now in development to be a major motion picture.

    Over 2,000,000 copies sold worldwide * Translated in 23 languages * Published in 32 countries
    ''',
    author = "AG Riddle",
    isbn = "B00C2WDD5I",
    category = 1,
    user_id = ruser,
    )
sess.add(book2)
sess.commit()

book2 = Books(
    title = "Born a Crime: Stories from a South African Childhood",
    image = "https://images-na.ssl-images-amazon.com/images/I/51vv5sw2N2L._SX327_BO1,204,203,200_.jpg",
    description = u'''"One of the comedy world's fastest-rising stars tells his wild coming-of-age story during the twilight of apartheid in South Africa and the tumultuous days of freedom that followed. Noah provides something deeper than traditional memoirists: powerfully funny observations about how farcical political and social systems play out in our lives.

    Trevor Noah is the host of The Daily Show with Trevor Noah, where he gleefully provides America with its nightly dose of serrated satire. He is a light-footed but cutting observer of the relentless absurdities of politics, nationalism, and race - and in particular the craziness of his own young life, which he's lived at the intersections of culture and history.

    In his first book, Noah tells his coming-of-age story with his larger-than-life mother during the last gasps of apartheid-era South Africa and the turbulent years that followed. Noah was born illegal - the son of a white Dutch father and a black Xhosa mother, who had to pretend to be his nanny or his father's servant in the brief moments when the family came together. His brilliantly eccentric mother loomed over his life - a comically zealous Christian (they went to church six days a week and three times on Sunday), a savvy hustler who kept food on their table during rough times, and an aggressively involved, if often seriously misguided, parent who set Noah on his bumpy path to stardom.

    The stories Noah tells are sometimes dark, occasionally bizarre, frequently tender, and always hilarious - whether he's subsisting on caterpillars during months of extreme poverty or making comically pitiful attempts at teenage romance in a color-obsessed world; whether he's being thrown into jail as the hapless fall guy for a crime he didn't commit or being thrown by his mother from a speeding car driven by murderous gangsters.
    ''',
    author = "Trevor Noah",
    isbn = "B01IW9TM5O",
    category = 3,
    user_id = ruser,
    )
sess.add(book2)
sess.commit()

book2 = Books(
    title = "Shaken: Discovering Your True Identity in the Midst of Life's Storms",
    image = "https://images-na.ssl-images-amazon.com/images/I/51wedO-9xuL._SX331_BO1,204,203,200_.jpg",
    description = u'''"Who are you when life is steady?
    Who are you when storms come?

    Most of us have been on the receiving end of rejection, a broken dream, or heartbreak. And while this is not an easy space to go through, when we are grounded in the truth, we can endure the tough times.

    In this powerful book, Heisman Trophy winner Tim Tebow passionately shares glimpses of his journey staying grounded in the face of disappointment, criticism, and intense media scrutiny. Following an exceptional college football career with the Florida Gators and a promising playoff run with the Denver Broncos, Tebow was traded to the New York Jets. He was released after one season.

    In Shaken, Tebow talks about what he’s learned along the way, building confidence in his identity in God, not the world. This moving book also features practical wisdom from Scripture and insights gained from others who have impacted Tebow in life-changing ways.

    Though traveling hard roads is not easy, it’s always worth it!
    ''',
    author = "Tim Tebow",
    isbn = "0735289867",
    category = 4,
    user_id = ruser,
    )
sess.add(book2)
sess.commit()

book2 = Books(
    title = "D DAY Through German Eyes - The Hidden Story of June 6th 1944",
    image = "https://images-na.ssl-images-amazon.com/images/I/51HquFVhKRL.jpg",
    description = u'''This is the hidden side of D Day which has fascinated readers around the world.

    Almost all accounts of D Day are told from the Allied perspective, with the emphasis on how German resistance was overcome on June 6th 1944. But what was it like to be a German soldier in the bunkers and gun emplacements of the Normandy coast, facing the onslaught of the mightiest seaborne invasion in history?
    What motivated the German defenders, what were their thought processes - and how did they fight from one strong point to another, among the dunes and fields, on that first cataclysmic day? What were their experiences on facing the tanks, the flamethrowers and the devastating air superiority of the Allies?

    This book sheds fascinating light on these questions, bringing together statements made by German survivors after the war, when time had allowed them to reflect on their state of mind, their actions and their choices of June 6th.

    We see a perspective of D Day which deserves to be added to the historical record, in which ordinary German troops struggled to make sense of the onslaught that was facing them, and emerged stunned at the weaponry and sheer determination of the Allied soldiers. We see, too, how the Germans fought in the great coastal bunkers, perceived as impregnable fortresses, but in reality often becoming tombs for their crews.

    Above all, we now have the unheard human voices of the individual German soldiers - the men who are so often portrayed as a faceless mass.
    ''',
    author = "Holger Eckhertz",
    isbn = "B00VX372UE",
    category = 5,
    user_id = ruser,
    )
sess.add(book2)
sess.commit()



books = sess.query(Books).all()
print "The following titles were added:"
for b in books:
    print b.title












