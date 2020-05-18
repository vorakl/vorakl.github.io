The zoo of binary-to-text encoding schemes
##########################################

:summary: A stream encoding algorithm with a variable base (16, 32, 36, 64, 58, 85, 94)
:date: 2020-05-13 20:01:53
:category: article
:tags: cs, programming, binary-to-text, encoding
:slug: stream-encoding

In `the previous article`_, I discussed the use of `the positional numeral system`_ for the purpose of `binary-to-text translation`_. That method represents a binary file as a single big number with the radix_ 256 and then converts this big number to another one with an arbitrary radix (base) in a range from 2 to 94. Although this approach gives the minimum possible size overhead, unfortunately, it also has a number of downsides which make it hardly usable in a real-world situation. In this article, I'll show what is used in practice, which encodings could be found in the wild, and how to build your own encoder.

|

What's wrong with the positional single number encoding?
========================================================

The main issue with converting a file as a big number in *radix 256*  to another big number with a smaller radix is that you need to read the whole file, load it to the memory and build actually that big number from each byte of the file. To construct a number, the `Least Significant Byte`_ (LSB), which is the last byte of a file, needs to be read and loaded. Although, there is not always enough memory to load a whole file as well as there is not always the whole file is available at any given time. For instance, if it's being transmitted over a network and only a small amount of bytes from the beginning (from the `Most Significant Byte`_, MSB) has been loaded. This issue is usually addressed by processing a file as a **stream of bytes**, in chunks, which then are being converted in the same way (by converting a number from one base to another). These chunks are much smaller and, ideally, fit the CPU registers' size (up to 8 bytes). The only question here is how to find the best size and ratio of such chunks (input and output) to keep the size overhead as closely as possible to a minimum available by treating files as big numbers.

|

What's the essence of a positional numeral system?
==================================================

In the positional numeral systems, everything turns around a *radix* (base) which shows how many different symbols are used to represent values. The actual glyph doesn't matter. Only their quantity. All these symbols are grouped in an alphabet (a table) where every symbol is defined by its own position, and this position represents its value. As long as counting starts from 0, the maximum symbol's value, in any numeral system, is always *radix - 1*. For instance, in the numeral system with a *radix 10* (Decimal), the maximum value has a symbol '9'. But, for a system with a *radix 2* (Binary), the maximum value has a symbol '1'. When symbols from an alphabet appear as a part of a number, they are called *digits*. A digit's position, in this case, is called *index* and defines the power of a radix while its value (position in the alphabet) defines a coefficient within the power of that radix. 

|

*The first crucial conclusion* here is that any number, represented in some positional numeral system, gets its meaning only when is known its radix. 

|

*The second conclusion* is not so obvious. Humans in most cases nowadays use the Decimal numeral system. Numbers gain more sense for them when they are represented as Decimal numbers and this is the system that is used the most for calculations. To any symbol in an alphabet is assigned its certain position which is a number with some radix. In most cases, this radix is 10 (Decimal). The Decimal numeral system is a temporary system that is used for converting one numeral system to another. Every time, when a number is defined by a radix, this radix is Decimal, no matter what's the radix of a number. Every time, when there is a need to convert a number X with radix M to a number Y with radix M, both numbers (X and Y) are represented by some certain alphabets (which define symbols with values), but their radixes (M and N) are always represented in Decimal system, thus, Decimal system is used as an intermediate numeral system to which a number X is converted first, and then the intermediate number is converted to a number Y. The intermediate numeral system could have been any radix, but *radix 10* is what people use for calculations and that's what can be found in most converters implementations.

|

*The third conclusion* is even more important. Symbols don't bring any value, only their position in the alphabet. This means we need to know not only an actual number's representation but also its radix and an alphabet - the table that contains symbols assigned to values (position within the table). A good example is `an alphabet of 16 symbols for Hexadecimal numbers`_ (*radix 16*). There are first 10 digits linked to equivalent values, so the symbol '0' is linked to 0, '1' to 1, and so on up to the symbol '9' linked to 9. The rest 6 values (from 10 to 15) linked to English letter symbols (from 'A' to 'F'). And again, these values (positions in the table) are all Decimal numbers (*radix 10*). By the way, the table could have been different, but that's what is used by convention, so anyone is able to interpret Hexadecimal numbers in the same way.

|

Where does the overhead come from?
==================================

Let's take a look at a few examples. This is a number '123' that is represented by three symbols, but until we know a radix, it is not possible to understand its value. If the radix is 10 then it is 'one hundred twenty three' in the Decimal system and it can be calculated by `the formula`_ for converting a numeral system with any radix to *radix 10* (because all numbers in this formula have radix 10): ``1*10^2 + 2*10^1 + 3*10^0 = 123``. If the radix is 8, then it is an Octal system and it is constructed as ``1*8^2 + 2*8^1 + 3*8^0`` which gives us a Decimal number 83. So, *'123 base 8'* equals to *'83 base 10'*. It is worth noticing that converting a number to a higher radix leads to lower a number of symbols needed for its representation. The converse is also true. If a number 83 with a *radix 10* is converted to a *radix 2*, it gets a form '1010011'. Notice, the radix is changed from 10 to 2 and the number of symbols changed from 2 to 7! As lower a radix gets, as more symbols appear in representation.

|

Let's get back to binary files. What we can determine as 'symbol representation' or 'digits', 'alphabet', and 'radix' based on a structure of an ordinary file? Any file consists of bytes as it is the minimum addressable group of bits. It cannot be less than 8 bits. So, we can think about a number representation as of some amount of bytes. The chunks can vary from 1 byte to a file's size. For example, if there is only one byte, then the number consists of only one digit. One byte or 8 bits (binary digits with a *radix 2*) allows one to represent ``2^8 = 256`` different numbers. That means, we can persist 256 different symbols with their positions to build an alphabet. The good news, such a table has already been standardized many years ago and called ASCII_. And the last thing, as the alphabet size is 256 symbols then a radix is also 256. Here is our number: a number of bytes in the chunk that we are going to process are the number of digits, a radix is 256, and the coefficient has a range from 0 to 255. For example, if a group of bytes to read from a stream and process at once consists of 4 bytes (from MSB to LSB): *[13, 200, 3, 65]* then our number can be represented as a Decimal number (*radix 10*) as ``13*256^3 + 200*256^2 + 3*256^1 + 65*256^0 = 231211841``

|

As it was discussed in `the previous article`_, we can use no more than 94 different symbols to reliably represent texts. Thus, the desired radix lies somewhere in the range from 2 to 94. Even 94 is much less than 256, so a number's representation in a new radix is likely to have more symbols. This means, in turn, that the output group will have more bytes as it is a minimum amount of data we can operate on, even if a digit represented by a symbol needs fewer bits. You'll still need to allocate the whole byte for each symbol in the new radix number representation. Some amount of bits in such bytes will never be used. This is the root of inefficiency, and that's why it's highly important to find a good ratio of output to input byte groups. For instance, the most used nowadays Base64_ encoding converts binary files to texts by reading 3-bytes groups from the input stream, represents them as a 3-digits number with a *radix 256* (``log[256^3, 2] = 24`` bit), and then converts this number to a 4-digits number with a *radix 64* (``log[64^4, 2] = 24`` bit), which in turn is written to the output stream as a group of 4 bytes. So, the ratio of output to input is ``4/3 = 1.333333``. In other words, the size overhead is 33.(3)%. There are a few considerations behind the logic of choosing the exact combination of input and output groups for a streaming conversion, which includes a target radix, a desirable/available alphabet, an ability to natively compute on a CPU, etc.

|

How to calculate a minimal overhead?
====================================

Let's calculate first, how many digits of a target base (radix) are needed to represent exactly the same number in the initial base. For instance, there is given a number 123 with a radix 10. How many bits (binary digits, a radix 2) are needed to represent the same decimal number? Every digit is a coefficient of power of a base. If it is not enough, one more base is added in power +1 to finally construct a number. Keeping in mind that counting starts from 0, if it's said that to represent some number 8 bit are needed, this means all bases in powers from 0 to 7 with their coefficients have to be summed up. Thus, to find out a number of digits needed to represent the number in some radix, we need to find an exponent, to which a new radix needs to be exponentiated. In our case,  for a base-10 number 123, we need to calculate an exponent of a base-2 by using a logarithm function: ``log[123, 2] = 6.9425145``. This means, to represent a number 123 with base 10, a little bit less than 7 bits will be enough. All computer systems operate on a set of `natural numbers`_ only. It is not possible to use 6.9425145 bits as this number is an approximated value of needed bits. 6 bits apparently won't be enough (``2^6 = 64``, which is much less than 123), so the only right approach is always to round up (by calling a *ceil* function) any non-integer values. Unfortunately, 7 bits are able to represent a bigger number (``2^7 = 128``) and this again contributes to a final overhead.

|

Let's have a look at the Base64 again. We know already (but not why is that, yet), that this streaming system uses 3 input bytes (a 3-digit number with a *base 256*) and converts them to a number with a *base 64*. How many base-64 digits will this number contain? The answer is ``log[256^3, 64] = 4``, four digits, hence 4 symbols from the base64 alphabet.

|

While looking for the good input and output group sizes it's good to know a theoretically possible minimum of the overhead. To find it out, we need to do a similar calculation but take the minimally possible amount of input data, which is one byte (8 bits, decimal ``2^8 = 256``). For the Base64, it is ``log[256, 64] = 1.33(3)``, that is again 33.(3)%. For the Base32_ it is ``log[256, 32] =  1.6``, that is 60%. And for the Base16_ it is ``log[256, 16] = 2``, that is 100%. Wow! These theoretical numbers are exactly the same as practically used ratios of output bytes to input bytes give. Here are they: for the Base64 it is ``4 / 3 = 1.33(3)``, for the Base32 it is ``8 / 5 = 1.6``, and for the Base16 it is ``2 / 1 = 2``. There is one interesting fact, all these three bases (16, 32, 64) have one thing in common - they all are powers of two! This leads us to the conclusion that converting numbers within the "power of two" bases allows one to get the best possible ratio and match precisely an input bits group to an output bits group. Although it is not always desirable or even possible. Sometimes there is a need to use a specific alphabet, e.g. in Base36_, or the minimal overhead, e.g. in Base85_ or Base94_. All these bases are not the "powers of two", so a tradeoff has to be found to minimize the overhead.

|

How to calculate optimal input and output groups?
=================================================

Alright, we've calculated a number of digits needed to represent some number in another base. But, why is that only a theoretical minimum? Why in practice it would need more? And, why would we still need to find a good ratio of output to input byte groups? To answer these questions, let's have a look at the **Base85** encoding. To represent 1 byte (Base256) of information in Base85, it needs ``log[256, 85] = 1.24816852`` digits. But, we can't use 1.248 digits. Only positive whole numbers are available! 1 digit is neither possible (too little). Then, 2 digits are the only way to go. In other words, to represent 1 byte (with a number in Base256), in fact, we'd need 2 bytes  (with a number in Base85), where ~75% of space will be wasted, as the ratio is ``2/1 = 2`` and this is a 100% overhead, instead of a theoretical 24.8%. There is no point to use 1-byte input group and 2-bytes output group. Thus, there should be some good input and output groups so their ratio goes as close as possible to a calculated minimum or even match it!

|

The following approach starts from 1-byte group and using the same formula, every time checks a number of digits in the destination base. if it's not close enough, increments the input group by 1 byte and checks again. You can decide on your own, what is the applicable size of an input group and how close to the whole number up (ceil function) the output group needs to be.

| 

This code goes through all bases, from 2 to 94, and prints a first found input/output group that has a delta between the number of digits and its rounded value less or equal 0.1, if any. That is, ``ceil(x) - x <=0.1``. I limited an input group by 20 bytes but in reality, groups larger than 8 bytes (64bit) will require either a `more complicated implementation`_ still based on 64bit variable types, or the big number mathematics which would bring it back to the solution from `the previous article`_.

|

.. code-block:: python

    from math import log, ceil

    def find_dec_fractions(num):
        for i, k in [(i, log(256**i, num)) for i in range(1,20)]:
            if (ceil(k)-k)<=0.1:
                return (i, k)

    for i in range(2, 95):
        try:
            b_in, b_out = find_dec_fractions(i)
        except TypeError:
            continue
        print(f'Base{i}: output/input {b_out} / {b_in}; Ratio: {ceil(b_out)} / {b_in} = {ceil(b_out)/b_in}')

|

.. code-block:: output

    Base2: output/input 8.0 / 1; Ratio: 8 / 1 = 8.0
    Base3: output/input 95.90132254286152 / 19; Ratio: 96 / 19 = 5.052631578947368
    Base4: output/input 4.0 / 1; Ratio: 4 / 1 = 4.0
    Base6: output/input 30.948224578763327 / 10; Ratio: 31 / 10 = 3.1
    Base7: output/input 19.94760247804924 / 7; Ratio: 20 / 7 = 2.857142857142857
    Base8: output/input 8.0 / 3; Ratio: 8 / 3 = 2.6666666666666665
    Base9: output/input 42.9032232428591 / 17; Ratio: 43 / 17 = 2.5294117647058822
    Base10: output/input 40.940079410301436 / 17; Ratio: 41 / 17 = 2.411764705882353
    Base11: output/input 6.937555831629307 / 3; Ratio: 7 / 3 = 2.3333333333333335
    Base12: output/input 8.926174260836154 / 4; Ratio: 9 / 4 = 2.25
    Base13: output/input 12.971431412511347 / 6; Ratio: 13 / 6 = 2.1666666666666665
    Base14: output/input 18.910766522677935 / 9; Ratio: 19 / 9 = 2.111111111111111
    Base15: output/input 38.905619771091956 / 19; Ratio: 39 / 19 = 2.0526315789473686
    Base16: output/input 2.0 / 1; Ratio: 2 / 1 = 2.0
    Base17: output/input 1.957204336945808 / 1; Ratio: 2 / 1 = 2.0
    Base18: output/input 1.9184997325450517 / 1; Ratio: 2 / 1 = 2.0
    Base19: output/input 16.949441762397953 / 9; Ratio: 17 / 9 = 1.8888888888888888
    Base20: output/input 12.957179936946513 / 7; Ratio: 13 / 7 = 1.8571428571428572
    Base21: output/input 10.928171937453742 / 6; Ratio: 11 / 6 = 1.8333333333333333
    Base22: output/input 8.969752968703016 / 5; Ratio: 9 / 5 = 1.8
    Base23: output/input 15.916660520940269 / 9; Ratio: 16 / 9 = 1.7777777777777777
    Base24: output/input 6.97933734353701 / 4; Ratio: 7 / 4 = 1.75
    Base25: output/input 18.949768555229294 / 11; Ratio: 19 / 11 = 1.7272727272727273
    Base26: output/input 11.913778998988336 / 7; Ratio: 12 / 7 = 1.7142857142857142
    Base27: output/input 26.919669485715517 / 16; Ratio: 27 / 16 = 1.6875
    Base28: output/input 4.992350344236227 / 3; Ratio: 5 / 3 = 1.6666666666666667
    Base29: output/input 4.940323979050427 / 3; Ratio: 5 / 3 = 1.6666666666666667
    Base30: output/input 17.933964143964545 / 11; Ratio: 18 / 11 = 1.6363636363636365
    Base31: output/input 12.91834154125439 / 8; Ratio: 13 / 8 = 1.625
    Base32: output/input 8.0 / 5; Ratio: 8 / 5 = 1.6
    Base33: output/input 7.929594526822421 / 5; Ratio: 8 / 5 = 1.6
    Base35: output/input 10.917705226052034 / 7; Ratio: 11 / 7 = 1.5714285714285714
    Base36: output/input 13.926701060443497 / 9; Ratio: 14 / 9 = 1.5555555555555556
    Base37: output/input 19.963706880682256 / 13; Ratio: 20 / 13 = 1.5384615384615385
    Base38: output/input 25.91499209004118 / 17; Ratio: 26 / 17 = 1.5294117647058822
    Base41: output/input 2.9864385798230937 / 2; Ratio: 3 / 2 = 1.5
    Base42: output/input 2.9671843746459023 / 2; Ratio: 3 / 2 = 1.5
    Base43: output/input 2.9486213303792987 / 2; Ratio: 3 / 2 = 1.5
    Base44: output/input 2.930708014618138 / 2; Ratio: 3 / 2 = 1.5
    Base45: output/input 2.913406407519012 / 2; Ratio: 3 / 2 = 1.5
    Base46: output/input 15.93174851664354 / 11; Ratio: 16 / 11 = 1.4545454545454546
    Base47: output/input 12.96225551928187 / 9; Ratio: 13 / 9 = 1.4444444444444444
    Base48: output/input 22.918685664133292 / 16; Ratio: 23 / 16 = 1.4375
    Base49: output/input 9.97380123902462 / 7; Ratio: 10 / 7 = 1.4285714285714286
    Base50: output/input 9.922293927591243 / 7; Ratio: 10 / 7 = 1.4285714285714286
    Base51: output/input 16.92397770133268 / 12; Ratio: 17 / 12 = 1.4166666666666667
    Base53: output/input 6.983337201921797 / 5; Ratio: 7 / 5 = 1.4
    Base54: output/input 6.9506137148575995 / 5; Ratio: 7 / 5 = 1.4
    Base55: output/input 6.918787617803083 / 5; Ratio: 7 / 5 = 1.4
    Base56: output/input 17.9083251145862 / 13; Ratio: 18 / 13 = 1.3846153846153846
    Base57: output/input 10.97226243673046 / 8; Ratio: 11 / 8 = 1.375
    Base58: output/input 10.925265898478088 / 8; Ratio: 11 / 8 = 1.375
    Base59: output/input 14.959262233248435 / 11; Ratio: 15 / 11 = 1.3636363636363635
    Base60: output/input 18.960906451063522 / 14; Ratio: 19 / 14 = 1.3571428571428572
    Base61: output/input 22.93138142177215 / 17; Ratio: 23 / 17 = 1.3529411764705883
    Base64: output/input 4.0 / 3; Ratio: 4 / 3 = 1.3333333333333333
    Base65: output/input 3.9851435091825076 / 3; Ratio: 4 / 3 = 1.3333333333333333
    Base66: output/input 3.9706212940573997 / 3; Ratio: 4 / 3 = 1.3333333333333333
    Base67: output/input 3.9564205613318486 / 3; Ratio: 4 / 3 = 1.3333333333333333
    Base68: output/input 3.942529199089205 / 3; Ratio: 4 / 3 = 1.3333333333333333
    Base69: output/input 3.9289357306851747 / 3; Ratio: 4 / 3 = 1.3333333333333333
    Base70: output/input 3.9156292724042583 / 3; Ratio: 4 / 3 = 1.3333333333333333
    Base71: output/input 3.9025994945192193 / 3; Ratio: 4 / 3 = 1.3333333333333333
    Base72: output/input 12.966121951449782 / 10; Ratio: 13 / 10 = 1.3
    Base73: output/input 12.92443739543971 / 10; Ratio: 13 / 10 = 1.3
    Base74: output/input 21.90208895887644 / 17; Ratio: 22 / 17 = 1.2941176470588236
    Base75: output/input 8.990468784305198 / 7; Ratio: 9 / 7 = 1.2857142857142858
    Base76: output/input 8.962972102269996 / 7; Ratio: 9 / 7 = 1.2857142857142858
    Base77: output/input 8.935999277516537 / 7; Ratio: 9 / 7 = 1.2857142857142858
    Base78: output/input 8.909533240680473 / 7; Ratio: 9 / 7 = 1.2857142857142858
    Base79: output/input 13.959876384572452 / 11; Ratio: 14 / 11 = 1.2727272727272727
    Base80: output/input 13.919804002700841 / 11; Ratio: 14 / 11 = 1.2727272727272727
    Base81: output/input 18.927892607143722 / 15; Ratio: 19 / 15 = 1.2666666666666666
    Base82: output/input 23.908573597131127 / 19; Ratio: 24 / 19 = 1.263157894736842
    Base85: output/input 4.9926740807112 / 4; Ratio: 5 / 4 = 1.25
    Base86: output/input 4.979564524879807 / 4; Ratio: 5 / 4 = 1.25
    Base87: output/input 4.966674008644963 / 4; Ratio: 5 / 4 = 1.25
    Base88: output/input 4.953996247544582 / 4; Ratio: 5 / 4 = 1.25
    Base89: output/input 4.941525209635524 / 4; Ratio: 5 / 4 = 1.25
    Base90: output/input 4.929255102536434 / 4; Ratio: 5 / 4 = 1.25
    Base91: output/input 4.917180361275656 / 4; Ratio: 5 / 4 = 1.25
    Base92: output/input 4.905295636885699 / 4; Ratio: 5 / 4 = 1.25
    Base93: output/input 15.904186303494539 / 13; Ratio: 16 / 13 = 1.2307692307692308
    Base94: output/input 10.984670683283468 / 9; Ratio: 11 / 9 = 1.2222222222222223

|

Conclusions
===========

This output provides several interesting insights:

1. All the "power of two" bases, e.g. Base16/32/64, always have a whole number of required digits, as the source base is also the "power of two"! This simple fact makes it even easier to calculate the optimal groups by using a method of finding `LCM (Least Common Multiple)`_, also shown in `the previous article`_.

2. There are a few groups of adjacent bases that require the same number of digits but are different by the size of their alphabets. It seems reasonable to prefer smaller alphabets, as less special symbols lead to better readability, e.g. when an encoded text needs to be used within a value of some variable in a programming language, or read verbally over a voice channel (encoded license keys).

3. Usually, the size of binary files, and especially executable files, appears to be evenly divisible by 4. This makes reasonable to use bases, that have 4-byte input groups. Then, there will be fewer chances to convert files, where the last byte group doesn't have all the needed data to perform the conversion. Although, even if it happens, it usually addresses using padding by NULL-symbols. The `Base32 and Base64 for padding`_ uses one extra symbol (out of the alphabet) '=', and `Ascii85 uses an even smarter approach`_, with no extra symbols on the output stream.

4. Among all bases in the list, there is one outstanding base, Base85. It uses 4 input bytes that aligned with the average case of binary files. 5 output bytes give only 25% overhead which provides better efficiency than Base64 (with its 33.3%). Both groups fit CPU's registers all modern computers. All these factors make this encoding much more optimal for a binary-to-text encoding than commonly used nowadays on the Internet encoding - Base64 or some times ago on the FidoNet_ - UUEncode_ (which internally is the same Base64). With the differences in alphabets, Base85 is used in PDF_, Git_, ZeroMQ_, and also implemented in the `Standard Python Library base64`.

5. There are also known to be used Crockford-Base32_, Base36_ and Base58_ in special applications, as efficiency is not the main consideration for their use and they meet other requirements.

|

.. Links
.. _`the previous article`: https://vorakl.com/articles/base94/
.. _`the positional numeral system`: https://en.wikipedia.org/wiki/Positional_notation
.. _`binary-to-text translation`: https://en.wikipedia.org/wiki/Binary-to-text_encoding
.. _radix: https://en.wikipedia.org/wiki/Radix
.. _`Least Significant Byte`: https://en.wikipedia.org/wiki/Bit_numbering#Least_significant_byte
.. _`Most Significant Byte`: https://en.wikipedia.org/wiki/Bit_numbering#Most_significant_byte
.. _ASCII: https://www.ascii-code.com/
.. _`an alphabet of 16 symbols for Hexadecimal numbers`: https://tools.ietf.org/html/rfc4648#page-11
.. _`the formula`: https://en.wikipedia.org/wiki/Positional_notation#Base_of_the_numeral_system
.. _Base64: https://tools.ietf.org/html/rfc4648#section-4
.. _Base32: https://tools.ietf.org/html/rfc4648#section-6
.. _Base16: https://tools.ietf.org/html/rfc4648#section-8
.. _Base36: https://en.wikipedia.org/wiki/Base36
.. _Base58: https://www.johndcook.com/blog/2019/03/04/base-58-encoding-and-bitcoin-addresses/
.. _Base85: https://www.johndcook.com/blog/2019/03/05/base85-encoding/
.. _Base94: https://gist.github.com/iso2022jp/4054241
.. _`natural numbers`: https://vorakl.com/articles/numbers/
.. _`more complicated implementation`: https://gist.github.com/iso2022jp/4054241
.. _`LCM (Least Common Multiple)`: https://en.wikipedia.org/wiki/Least_common_multiple
.. _`Ascii85 uses an even smarter approach`: https://en.wikipedia.org/wiki/Ascii85#Adobe_version
.. _`Base32 and Base64 for padding`: https://tools.ietf.org/html/rfc4648#section-3.2
.. _UUEncode: https://en.wikipedia.org/wiki/Uuencoding
.. _ZeroMQ: https://rfc.zeromq.org/spec/32/
.. _Git: https://github.com/git/git/blob/53f9a3e157dbbc901a02ac2c73346d375e24978c/base85.c
.. _PDF: https://en.wikipedia.org/wiki/Ascii85
.. _Crockford-base32: https://www.crockford.com/base32.html
.. _FidoNet: https://en.wikipedia.org/wiki/FidoNet
.. _`Standard Python Library base64`: https://github.com/python/cpython/blob/3.8/Lib/base64.py#L416
