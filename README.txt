-- DESIGN CHOICES --
Upon a brief inspection, I noticed that there are some null entries in the Variant Barcode section of the CSV file, so the first natural thing to do was to check whether such a product can exist. So, upon finding out that if you are the only seller of a product or if it is a store brand it may not need a GTIN, I treated it as such.

Additionally, I noticed that they differ in lengths, so I decided it was best to see whether 