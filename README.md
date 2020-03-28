# WordFreud

![WordFreud Logo](logo_200.png)

This is a password generating tool that offers flexibility when it comes to generating passwords based on someones (or somethings) background.
It has the following core features:

1. Passwords are generated based on a custom list of:
	* numbers that have a special meaning
	* words that have a special meaning
2. The ability to generate as many possible passwords based on that:
	* By being able to choose how individual words are *glued* together
	* By being able to substitute characters (letters) for special ch4r@ct3rs
	* By defining what gets prepended or appended
	* By defining the type of casing that should be applied

## Why another password generator tool

Most tools focus on simply making combinations based on dictionairies. However, when a user chooses a password often the same set of steps are taken, that have nothing to do with dictionairy files.

Suppose the password requirement is a minimum of 8 charachters. 

* A user might that loves apple pies might choose to use this as his/her password : `applepies`. So far, a dictionary might have worked.
* If the requirement is to have at least one uppercase character, the user might change this to `Applepies` or even `ApplePies`
* If another requirement would be to have at least 1 number in it, then the year of birth might be added `ApplePies1970`
* And if yet another requirement would be to have at least 1 special character in it, the user migth choose to simply at an exclamation point `ApplePies1970!`, or maybe substitute one or more characters `App!ePie$1970`

In itself, this is a very strong password, that would take about [3 million years](https://howsecureismypassword.net/) to crack and that you will probably not find in a dictionary file. However, for someone that knows the user it could still be relatively easy to guess. This tool exposes that danger.

## WordFreud?
This tool combines the psychological aspect of getting to know someone or something, with the puzzle of coming up with combinations that reflect this in a password.

# Installation

# Usage
In order to use this tool, you need to create a file with relevant words, seperated by a newline. When words belong together you put them on the same line though; for example `resevoir dogs`.

Optionally, you can also create a file that contain numbers with a special relevance, such as a date of birth

Then you will need to design how you want to make the variations. Invoking the tool with the `-h` parameter will display all the options:

```
usage: wordfreud.py input-file-with-words [input-file-with-numbers] [options]

positional arguments:
  wf                    Input file with words
  nf                    (optional) Input file with numbers

optional arguments:
  -h, --help            show this help message and exit
  -o O                  Output file. If omitted stdout is used
  --fullyear2shortyear  Full year to short year; add yy based yyyy (year)
  --year2age            Year to age; add (current) age based on year
  --offsetyear OFFSETYEAR
                        Offset year; this will be used to calculate the age of
                        any year that is found (instead of the current year).
                        Only works when -year2age flag is set
  -g G                  Glue; This determines which characters are used to
                        glue individual pieces together. Pass all characters
                        as a single string. Example: "_-." -> this will result
                        in 3 characters being used as glue: _, - & .
  -ga                   Glue All; in this mode, 'glue' is also put between
                        words and special characters and/or numbers
  -c C                  Special Characters
  -pc                   Prepend Character
  -ac                   Append Character
  -sm SM                Substitute Map
  -sl                   Substitute To Lowercase
  -su                   Substitute To Uppercase
  -sc                   Substitute To CamelCase
  -v                    Verbose
```

* **wf** : This is the file containing all the words. Every line in this file has to contain one word, but can contain multiple related words too (such as a first and last name or the title of a movie)
* **nf** : This is the file containing all the numbers (Optional)

* **o** : This is the output file. If it's omitted, the result will go to the standard output. When a file is used for the output, the program displays information about it's operations; when standard output is used, this information is hidden.
* **fullyear2shortyear** : If set, years in a short-notation (e.g. 70) get a variation in a full notation (1970)
* **year2age** : If set, a year will be converted in an age, relative to the current year (so, if the current year is 2020 and the year 70 (1970) is detected, another variation will be created with 50
* **offsetyear** : Will only be processed if **year2age** is specified. In that case the noy-specified year will be used to calculate the age
* **g** : When a line in the word-file (wf parameter) contains multiple words, they will be *glued* together. By default the characters `_`, `-` & `.` are used, but you can decide to customize this. Simply put them all in a string together and pass them as the argument. For example, if you want to use the characters `.` & `|`, then pass `'.|'` as the value for this argument.<br>It could also be that you simply want to glue them together without any character in between : in this case pass an empty value `''`<br>
Please note that a version with and without spaces will always be generated, regardless of the glue.
* **ga** : This flag will use the glue specified by the **g** parameter to glue not only multiple words, but also the numbers and special characters. It will create as many variations as possible of course.
* **c** : Special characters that will be used to create variations, such as `!` or `@`. You can pass them as a single value on the command-line `'!@'` and decide if they should be *prepended* or *appended* by using the **pc** and **ac** flags. This will then result in *[word]!* or *![word]*. When neither **pc** nor **ac** is set, these characters are appended by default (as if **ac** was set)
* **pc** : If set, special characters defined by the -c parameter will be prepended. This can be used in combination with **ac**
* **ac** : If set, special characters defined by the -c parameter will be appended. This is the default when neither **ac** nor **pc** is set explicitly. Can be used in combination with **pc**
* **sm** : String containing a map for substitutions of characters. For example, to create a variation where an a is transformed into a @. Multiple substitutions are separated by a comma; first character will be substituted by the second character. Example: `"a@,e3,i1,o0"`
* **sl** : If set, an all-lowercase variation of every combination is made
* **su** : If set an a variation with a Capital is made of every combation
* **sc** : If set, when multiple words are glued together, every part will get a Capital: LikeThis.


# Karma Guardian
This software is protected with a [Karma Guardian](https://www.karmaguardian.org).
It should not be used for purposes with bad intent. Using it for malicious purposes means you will need to face the consequences. *Karma Style*
