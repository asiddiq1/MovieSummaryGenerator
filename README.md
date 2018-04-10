# MovieSummaryGenerator

This project uses text summarization to create a movie summary from a set of movie reviews. Four different algorithms were implemented to produce multiple summaries for each movie. My first, most basic algorithm is a baseline method that creates summaries based on random selections of sentences from my review set. Beyond this, I implemented algorithms based off of Luhn’s Auto Abstract Algorithm, Tf-idf (Term Frequency-Inverse Document Frequency), and Tf-idf for nouns, (all of which will be elaborated on in a later section). The accuracy of these algorithms were then evaluated via a user study where users were asked which summary reflected the plot of the movie the most. In addition, users were asked if the results generated for Tf-idf and Tf-idf for nouns were similar, meaning if the same sentences were used in both of them.


Dataset Input: 

product/productId: B00742GOP2
review/userId: A39QGLA6AN181X
review/profileName: Brigetta Barone "BB"
review/helpfulness: 1/2
review/score: 5.0
review/time: 1335571200
review/summary: Awesome film!!!!

review/text: This movie took it's time developing characters and plot, but then it has you sitting on the edge of your seat. It essentially explains how the 'zombie' virus starts, and it does so very realistically. We loved it.

product/productId: 0790747324
review/userId: A1LS8REVM1FGCX
review/profileName: Ma Magdalena Lozano
review/helpfulness: 1/2
review/score: 5.0
review/time: 1258761600
review/summary: great classic movie

review/text: This is a good fantasy movie. Rod Taylor is terrific in his role as is Yvette Mimeux. If you want action and adventure, this is the movie for you.


Example of outputs depending on algorithm used: 

======TFIDF with length taken into account======
Payback tells the story of a gangster named Porter (Mel Gibson) who was working alongside his wife Lynn (Deborah Kara Unger) and his friend Val Resnick (Gregg Henry) until one day, shortly after stealing $140,000-to be split 50/50 between Porter and Resnick- from the Chinese mob, he was shot in the back repeatedly by Lynn and beaten by Resnick. I really didn't care if the Mel Gibson character (Porter) got his money or not. Career criminals Porter (Mel Gibson) and Val (Gregg Henry) rob a gang of $140,000. Mel Gibson plays the role of Porter who is mean, ruthless and dangerous. Mel Gibson's Porter is the quintessential antihero. 

======TFIDF using only nouns and length taken into account======
Porter (Gibson) Is even more hard core in this version. "Nonsense," Porter says. Porter does, $70,000. I really didn't care if the Mel Gibson character (Porter) got his money or not. Payback tells the story of a gangster named Porter (Mel Gibson) who was working alongside his wife Lynn (Deborah Kara Unger) and his friend Val Resnick (Gregg Henry) until one day, shortly after stealing $140,000-to be split 50/50 between Porter and Resnick- from the Chinese mob, he was shot in the back repeatedly by Lynn and beaten by Resnick. 

======Luhn======
plenty of action in this flick, plenty of familiar faces in the acting dept also, don't expect an academy award winner, but...if ya seen it at the movies on a saturday afternoon, it was well worth the money.. soap star trevor st john plays a hot guy, the son of kris kristofferson, william devane plays a outfit boss, corrupt cops....has everything in this movie to keep ya entertained....a comparison to " get carter" with stallone was mentioned, i was seeing the same exact thing, this was much better, mel gibson has 9 live in this movie for sure Grimy, violent, funny, smoke-filled tribute to bad guys from vintage movies, this film features another captivating performance by Mel Gibson, in a radically different role for him, an entertaining story, a distinct finger-snapping musical score, and an overall fun guy-time at the movies! Payback tells the story of a gangster named Porter (Mel Gibson) who was working alongside his wife Lynn (Deborah Kara Unger) and his friend Val Resnick (Gregg Henry) until one day, shortly after stealing $140,000-to be split 50/50 between Porter and Resnick- from the Chinese mob, he was shot in the back repeatedly by Lynn and beaten by Resnick. Maria Bello (THE DARK, A HISTORY OF VIOLENCE) plays a high-priced call-girl and Porter's only friend, Lucy Liu (KILL BILL) is the hilariously wicked sado-masochistic dominatrix, and the outfit bosses are played by William Devane, James Coburn, and Kris Kristofferson (THE JACKET). The story then goes a little bit complicated after : [1] dirty cops want to have share, [2] the China gang wants revenge, and [3] mob organization whom his partner give his money to. Created by Brian Helgeland, Payback is a superb, hard-hitting and atmospheric movie that boasts some excellent supporting performances which includes Gregg Henry as Val, Maria Bello as Rosie and David Paymer as Stegman. 

======Random Sentences======
The studio cut contained the "missing scenes" and revamped story line. Gibson, appearing more haggard and balding than ever, is quite appealing. It's just a bunch of stuff that happens, and it doens't really stand out in my mind over other action movies of the same sort. Porter's the lesser of the evils in Payback. Lucy Alexis Liu performs quite scarily as the masochistic/sadistic call girl with some interesting associates. William Devane, James Coburn, and Kris Kristofferson were wasted in this film. 







