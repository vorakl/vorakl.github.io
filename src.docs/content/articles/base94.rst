Convert binary data to a text with the lowest overhead
######################################################

:summary: A binary-to-text encoding with any radix from 2 to 94
:date: 2020-04-18 23:10:29
:category: article
:tags: cs, programming, binary-to-text, encoding
:slug: base94

This article is about `binary/text converters`_, the most popular implementations, and a non-standard approach which uses `the Place-Based Single Number Encoding`_ by representing a file as one big number and then converting it to another big number with any non-256 (1 byte/8 bit) radix. To make it applicable for a practical use, it makes sense to limit a radix (base) to 94 for matching numbers to all possible printable symbols within 7 bits ASCII_ table. It is likely a theoretical prototype and carries a pure academical flavor as the time and space complexities make it applicable only to small files (up to a few tens of kilobytes), although it allows one to choose any base with no dependencies on powers of two, e.g. 7 or 77.

Background
==========

The main purpose of such converters is to put a binary file, represented by 256 different symbols (radix-256, 1 byte, 2^8), to a form applicable for sending over a channel with a limited for transmission range of supported symbols. A good example is any text-based network protocol, like HTTP or SMTP, where all transmitted binary data has to be reversibly converted to a pure text form with no control symbols in it. As it's known, the ASCII codes from 0 to 31 are considered to be the control characters, and that's why they will definitely be lost while transmitting over any logical channel that doesn't allow endpoints to transmit full 8-bit bytes (binary) with codes from 0 to 255. This limits the number of allowed symbols to less than 224 (256-32), but in fact it's limited by only first 128 standartized symbols in the ASCII table and even more.

|

The standard solution nowadays for this purpose is the Base64 algorithm defined in the `RFC 4648`_ (easy reading). It also describes Base32 and Base16 as possible variations. The key point here: they all share the same characteristic as they are all powers of two. The wider a range of supported symbols (codes) the more space efficient result of conversion is. It will be bigger anyway, but the only question is how much bigger. For example, Base64 encoding gives an approximately 33% bigger output, because 3 input (8 valued bits) bytes are translated to 4 output (6 valued bits, 2^6=64) bytes. So, the ratio is always 4/3 that is the output is bigger by 1/3 or 33.(3)%. Practically speaking, Base32 is very inefficient because it implies translating 5 input (8 valued bits) bytes to 8 output (5 valued bits, 2^5=32) bytes and the ratio is 8/5, that is output is bigger by 3/5 or 60%. In this context, it is hard to consider any sort of efficiency of Base16 as its output size is bigger by 100% (each byte with 8 valued bits is represented by two 4 valued bits bytes, also know as the nibbles_, 2^4=16). It is not even a translation, but rather just a representation of an 8-bit byte in the hexadecimal view.

|

If you're curious, how these input/output byte ratios were calculated for the Base64/32/16 encodings, then the answer is the LCM (Least Common Multiple). Let's calculate them by ourselves, and for this, we'll need one more function, GCD (Greatest Common Divisor)

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

What's the point?
=================

The point is the following. What if a channel is able to transmit only just a few different symbols, like 9 or 17. That is, we have a file represented by 256 symbols alphabet (a normal 8-bit byte), we are not limited by computational power or memory constraints on both sides, but we are able to send only 7 different symbols instead of 256? Base64/32/16 are not a solution here. Then, Base7 is the only possible output format.

|

Another example, what if an amount of transmitted data is a concern for a channel? Base64, as it was shown, increases the data by 33% no matter what is transmitted, always. For instance, Base94 increases output by only 22%.

|

It might seem that Base94 is not the limit. If the first 32 ASCII codes are control characters and there are 256 codes in total, what stops one from using an alphabet of 256 - 32 = 224 symbols? There is a reason. Not all of 224 ASCII codes have printable characters. In general, only 7 bits (0..127) are standardized and the rest (128..255) is used for the variety of locales, e.g. Koi8-R, Windows-1251, etc. That means, only 128 - 32 = 96 are available in the standardized range. In addition, the ASCII code 32 is the space character and 127 doesn't have a visible character either. Hence, 96 - 2 gives us that 94 printable characters which have the same association with their codes on all possible machines.

Solution
========

`This solution`_ is pretty simple but this simplicity also puts a significant computational constraint. The whole input file can be treated as one big number with a radix (base) 256. It might easily be areally big number required thousands of bits. Then, we just need to convert this big number to a different base. That's it. And Python3 makes it even simpler! Usually, conversions between different bases are done via an intermediate Base10. The good news is that Python3 has built-in support for big numbers calculations (it is integrated with Int), and the Int class has a method that reads any number of bytes and automatically represents them in a big Base10 number with a desired endian. So, all these complications are able to be implemented in just two lines of code, which is pretty amazing!

.. code-block:: python

    with open('inpit_file', 'rb') as f:
        in_data = int.from_bytes(f.read(), 'big')

where in_data is our big number with Base10. These are just two lines but this is the point where most computation happens and the most time is consumed. So now, convert it to any other base as it's usually done with normal small decimal numbers.


.. Links
.. _`binary/text converters`: https://en.wikipedia.org/wiki/Binary-to-text_encoding
.. _`RFC 4648`: https://tools.ietf.org/html/rfc4648
.. _ASCII: https://www.ascii-code.com/
.. _nibbles: https://en.wikipedia.org/wiki/Nibble
.. _`This solution`: https://github.com/vorakl/base94
.. _`the Place-Based Single Number Encoding`: https://merrigrove.blogspot.com/2014/04/what-heck-is-base64-encoding-really.html
