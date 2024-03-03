Convert binary data to a text with the lowest overhead
######################################################

:summary: A binary-to-text encoding with any radix from 2 to 94
:date: 2020-04-18 23:10:29
:category: article
:tags: cs, binary-to-text, encoding
:slug: base94


This article discusses `binary/text converters`_, the most popular implementations, and a non-standard approach that uses `place-based single-number encoding`_ by representing a file as a large number and then converting it to another large number with any non-256 (1-byte/8-bit) radix. To make it practical, it makes sense to limit a radix (base) to 94 for matching numbers to all possible printable symbols within the 7-bit ASCII_ table. It is probably a theoretical prototype and has a purely academic flavor, as the time and space complexities make it applicable only to small files (up to a few tens of kilobytes), although it allows one to choose any base with no dependencies on powers of two, e.g. 7 or 77.

|

Background
==========

The main purpose of such converters is to convert a binary file represented by 256 different symbols (radix-256, 1 byte, 2^8) into a form suitable for transmission over a channel with a limited range of supported symbols. A good example is any text-based network protocol, such as HTTP (before ver. 2) or SMTP, where all transmitted binary data must be reversibly converted to a pure text form without control symbols. As you may know, ASCII codes from 0 to 31 are considered control characters, and therefore will definitely be lost during transmission over any logical channel that doesn't allow endpoints to transmit full 8-bit bytes (binary) with codes from 0 to 255. This limits the number of allowed symbols to less than 224 (256-32), but it's actually limited by the first 128 (2^7, 7 bits) standardized symbols in the ASCII table, and even more.

|

The standard solution today is the Base64 algorithm defined in `RFC 4648`_ (easy to read and understand). It also describes Base32 and Base16 as possible variants. The key point here is that they all share the same property of being powers of two. The wider the range of supported symbols (codes), the more space-efficient the result of the conversion. It will be larger anyway, the question is how much larger. For example, Base64 encoding gives about 33% larger output, because 3 input bytes (8 valued bits) are translated into 4 output bytes (6 valued bits, 2^6=64). So the ratio is always 4/3, i.e. the output is larger by 1/3 or 33.(3)%. Practically speaking, Base32 is very inefficient because it means translating 5 input bytes (8 valued bits) into 8 output bytes (5 valued bits, 2^5=32) and the ratio is 8/5, i.e. the output is larger by 3/5 or 60%. In this context, it is hard to consider any kind of efficiency of Base16, since its output size is larger by 100% (each byte of 8 valued bits is represented by two bytes of 4 valued bits, also known as nibbles_, 2^4=16). By the way, this is a well-used representation of 8-bit bytes, called hexadecimal.

|

If you're curious how these input/output byte ratios were calculated for
the Base64/32/16 encodings, the answer is LCM (Least Common Multiple). Let's
calculate it ourselves, and for that we need another function, the GCD (Greatest
Common Divisor)

|

1. Base64 (Input: 8 bits, Output: 6 bits):
    * LCM(8, 6) = 8*6/GCD(8,6) = 24 bit
    * Input: 24 / 8 = 3 bytes
    * Output: 24  / 6  = 4 bytes
    * Ratio (Output/Input): 4/3

2. Base32 (Input: 8 bits, Output: 5 bits):
    * LCM(8, 5) = 8*5/GCD(8,5) = 40 bit
    * Input: 40 / 8 = 5 bytes
    * Output: 40  / 5  = 8 bytes
    * Ratio (Output/Input): 8/5

3. Base16 (Input: 8 bits, Output: 4 bits): 
    * LCM(8, 4) = 8*4/GCD(8,4) = 8 bit
    * Input: 8 / 8 = 1 byte
    * Output: 8  / 4  = 2 bytes
    * Ratio (Output/Input): 2/1

|

The key problem
===============

What if a channel is only capable of transmitting a few different symbols, such as 9 or 17? That is, we have a file represented by a 256-symbol alphabet (a normal 8-bit byte), we are not really limited by computing power or memory constraints on either side, but we are only able to send 7 different symbols instead of 256? Base64/32/16 are not a solution here. Then Base7 is the only possible output format.

|

Another example, what if the amount of data transmitted is a concern for a channel? Base64, as it has been shown, increases the data by 33%, no matter what is transmitted, always. Base94, for example, only increases the output by 22%.

|

It may seem that Base94 is not the limit. If the first 32 ASCII codes are control characters, and there are 256 codes in total, what stops you from using an alphabet of 256 - 32 = 224 symbols? It turns out that there is a limit. Not all of the 224 ASCII codes are printable characters or have a standard representation. In general, only 7 bits (0..127) are standardized, and the rest (128..255) is used for the variety of locales, e.g. Koi8-R, Windows-1251, etc. This means that only 128 - 32 = 96 are available in the standardized range. In addition, the ASCII code 32 is the space character, and 127 doesn't have a visible character either. So 96 - 2 gives us the 94 printable characters that have the same association with their codes on most machines.

|

Solution
========

Although `This solution`_ is quite simple, this simplicity also imposes a significant computational constraint. The entire input file can be treated as a large number with a base of 256. It could easily be a really big number, requiring thousands of bits. Then all we have to do is convert that big number to a different base. That's it. And Python3 makes it even easier! Normally, conversions between different bases are done via an intermediate base10. The good news is that Python3 has built-in support for large number calculations. The int class has a method that reads any number of bytes and automatically represents them as a large Base10 number with a desired endian. So essentially all of this complexity can be implemented in just two lines of code!

.. code-block:: python

    with open('inpit_file', 'rb') as f:
        in_data = int.from_bytes(f.read(), 'big')

|

where *in_data* is the big Base10 number. That's only two lines, but that's where most of the math happens and most of the time is spent. So now convert it to any other base, as you'd normally do with normal small decimal numbers.

|

.. Links
.. _`binary/text converters`: https://en.wikipedia.org/wiki/Binary-to-text_encoding
.. _`RFC 4648`: https://tools.ietf.org/html/rfc4648
.. _ASCII: https://www.ascii-code.com/
.. _nibbles: https://en.wikipedia.org/wiki/Nibble
.. _`This solution`: https://github.com/vorakl/base94
.. _`place-based single-number encoding`: https://merrigrove.blogspot.com/2014/04/what-heck-is-base64-encoding-really.html
