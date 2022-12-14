# *Clima*tic - A weather inspired poetry generator


## What is *clima*tic?

Climatic seeks to create poetry based off weather/temperature of a given city. 

It is loosely inspired by the Spanish poetry genre [flamenca](https://www.writersdigest.com/write-better-poetry/flamenca-poetic-forms), which utilizes 5 lines of around 6 syllables to try to create rhythms like that of flamenco dancers clicking their feet and heels. <br>
*clima* is also one way to say weather in Spanish!

These poems are rewarded by fitness for having 6 syllables and for being about 5 lines, though some 6-liners and slightly more syllabic lines can also shine as well if they incorporate a weather feel. Fitness is also impacted by sentiment (if it captures the mood of certain weather events/temperatures) and if the poem includes weather-related words.

It utilizes weather/temperature in a given city to situation the poem as well as an inspiring set of poems that center around the weather, generated by a genetic algorithm that makes use of verb conjugations and noun substitutions, as well as word/formatting "experts" (outside objects).

# How to use: setup + running code

Climatic uses OpenWeatherMap-API to find the current temperature and weather of a city, which situates the mood for the poem (much like in [full FACE](https://www.yumpu.com/en/document/read/19102975/full-face-poetry-generation-computational-creativity) the poetry is situated in the mood of a given day.
If you don't have an OpenWeatherMap-API account, they are free and this just uses their most basic tier (free) API-- once you get a key, save it into `api_keys.py`. In the file, enter the following:
```
class API_Key():
    def __init__(self):
        self.API_KEY = "<YOUR KEY HERE>"
    
    def get_key(self):
        return self.API_KEY

```
 This class is imported into weather_call.py, the file that handles the weather API interactions.
 
 
 Before running, set up virtual environment by running `source venv6/bin/activate` or installing the requirements.txt. 
 Then to run, call `python3 main.py`. 
 You will be prompted for a city, and then you will be prompted for a stats file name so that if you'd like you can analyze the fitness over time of the poetry. Through doing this analysis, the best number of iterations seems to be around 15. Many generations stabilize in fitness early on, but a few have seen improvements later, so not capping it at 7 seemed like a good way to allow for potential improvements!
 
 Once you run, you have the choice of the last 3 poems to be read out loud. The poem you choose is saved to an mp3 file for later listening using afplay (built in Apple audio file player). 
 
 ### Analyzing Data
 To analyze any poetry data, call `python3 analyze_stats.py` and then type the stats file you would like to graph.
 Another evaluation metric is the delta from the target mood (delta closer to 0 means the poem is supposed to have a sentiment closer to the target mood).
 
 **Sample graphs**

     
    
 ![plot11102](https://user-images.githubusercontent.com/68559641/203139990-e32e206e-26c3-4b80-9adb-a8550af288bd.png)
 ![plot3095](https://user-images.githubusercontent.com/68559641/203140023-6848348b-f263-4a61-a72c-d33c4a75415d.png)
![plot36094](https://user-images.githubusercontent.com/68559641/203140061-61368b9c-5a5a-4055-9c69-55793ef673e7.png)


 
 ### Viewing poems
 Every poem created along the way is saved into the generated_poems file, so you can see any poem later!
 Poems are named by their "core nouns" and if poems have the same core nouns they are given the iteration/generation number at the end.

# How I challenged myself as a computer scientist

This was a challenging project for me, in terms of coming up with ideas and also coming up with ideas of proper scope.
I had thought about doing Spanish poetry generation and ended up with this poetry that is more loosely inspired-- this was a lesson in how complex the poetry problem is!

I used many new things:
<ul>
<li>learned how to untrack files on git for api_keys.py</li>
<li>used matplot lib for the first time for graphing fitness stats</li>
<li>utilized the pronouncing libraries and nltk POS tagging, as well as conjugation modules that lacked much documentation </li>
<li>OpenWeather API </li>
</ul>
I didn't give up on the project, but I had to adjust my sights to what was realistic in a given timeframe (especially regarding how many new things I learned and used). That was harder than I expected!
 
 In a further expansion I'd love to incorporate more of a rule-set or grammar, because sometimes the poems end up semantically confusing partly due to some more fanciful poetry in the inspiring set and largely due to the way crossover and line selection by fitness occurs.

# Scholarly Influences and Other Cited Resources

In terms of developing a human connection and situating the poetry in a place/waether, I was inspired by [full FACE](https://www.yumpu.com/en/document/read/19102975/full-face-poetry-generation-computational-creativity). 
In terms of the idea of having "experts" that specialized in different tasks, and identifying fittest lines (inspired by the idea of a "most inpsiring line in the paper), [this paper "Poetry Generation System with an Emotional Personality](https://www.researchgate.net/publication/274249704_Poetry_Generation_System_With_an_Emotional_Personality) helped guide me.
Also, I was loosely inspired to "bias the generation of verses according to a combination of different scoring functions" by [this paper](https://computationalcreativity.net/iccc21/wp-content/uploads/2021/09/ICCC_2021_paper_31.pdf) although I don't consider nearly as many complexities as the author. This paper also went fully into syllable generation with far more complex methods than I implemented but was a cool read.
    
 

## Other resources

[How to not expose your API keys](https://levelup.gitconnected.com/keep-api-keys-out-of-git-repositories-a-few-concrete-examples-80f2544789aa)<br>
[NLTK POS tags](https://stackoverflow.com/questions/15388831/what-are-all-possible-pos-tags-of-nltk )</br>
[Synonyms with WordNet](https://www.holisticseo.digital/python-seo/nltk/wordnet)
[Finding possible verbs to substitute](https://www.reddit.com/r/LanguageTechnology/comments/egh7jk/how_to_check_if_a_word_can_be_interpreted_as_a/)</br>
[See if a file exists already](https://www.pythontutorial.net/python-basics/python-check-if-file-exists/)
[Sample using mlconjug3 in english (documentation is mainly french examples)](https://github.com/tyxchen/bad-excuses-for-zoom-abuses/blob/master/excuses.py) 
[matplotlib help](https://stackoverflow.com/questions/18458734/how-do-i-plot-list-of-tuples-in-python)
[OpenWeatherAPI help](https://www.tutorialspoint.com/find-current-weather-of-any-city-using-openweathermap-api-in-python)
[More openweather API stuff](https://geekyhumans.com/get-weather-information-using-python/)
OpenWeatherAPI documentation on website too
