# One problem at Haidian Book City


Today, I just came by Haidian Book City as usual at Haidian dist in
    Beijing. and I found the problem hung on the wall nearby. It is very
    interesting and I want to share it.
<!--more-->

## **0x00 Problem**

Here is one picture of it.

![27-problem_at_haidian_book_city](https://user-images.githubusercontent.com/3297411/45277447-6ab6f900-b4fa-11e8-8201-8f9482f9e775.jpg)

A translation of that:

 > *Solve this problem, then it's your domain:*
 > *{3, 13, 1113, 3113,..., the 8<sup>th</sup> number}.angelcrunch.com*  
 > *(the QR code leads to the below link)*
 > *[www.angelcrunch.com/jiemi](http://www.angelcrunch.com/jiemi)*

Once you finish it, you will get the second as below:

 > *Guess a television series by the following numbers, and you will get an interview.*
 > *3113112211322112 / 311311*

## **0x01 Solution**

Yes, as you may guess, it is one look-and-say sequence(sequence [A006715](http://oeis.org/A006715) in 
[OEIS](http://en.wikipedia.org/wiki/On-Line_Encyclopedia_of_Integer_Sequences).

In the sewuence, each member is genrated from the previous menber by
"reading" off the digits in it, counting rhe number of digits in groups of
the same digit. For example:

 - 3 is reading off as "one 3" or 13.
 - 13 is reading off as "one 1 one 3" or 1113.
 - 1113 is reading off as "three 1s, then one 3" or 3113.
 - and so on.

If we start with any digit *d* from 0 to 9 then *d* will remain
indefinitely as the last digit of the sequence. For *d* different from 1, the
sequence starts as follows:

*d, 1d, 111d, 311d, 13211d, 111312211d, 31131122211d, ...*

As example in the following table.

<p>
    <table style="margin-right: auto; white-space: nowrap; width: auto;">
      <tr style="Text">
        <td align="left"><b><i>d</i></b></td>
        <td align="left"><b>Sloane</b></td>
        <td align="left"><b>sequence</b></td>
      </tr>
      <tr style="Text">
        <td align="left">1</td>
        <td align="left"><a href="http://oeis.org/A005150">A005150</a></td>
        <td align="left">1, 11, 21, 1211, 111221, 312211, 13112221, 1113213211, ...</td>
      </tr>
      <tr style="Text">
        <td align="left">2</td>
        <td align="left"><a href="http://oeis.org/A006751">A006751</a></td>
        <td align="left">2, 12, 1112, 3112, 132112, 1113122112, 311311222112, ...</td>
      </tr>
      <tr style="Text">
        <td align="left">3</td>
        <td align="left"><a href="http://oeis.org/A006715">A006715</a></td>
        <td align="left">3, 13, 1113, 3113, 132113, 1113122113, 311311222113, ...</td>
      </tr>
    </table>
</p>

Here, *d* equals 3.

So the first answer is 13211321322113.

For the second one, you need to know more about the sequence.
John Conway studied this sequence and found that the 8<sup>th</sup>
member and every member after it in the sequence is made up of one or more
    of 92 "basic" non-interacting subsequences. The 92 basic subsequence shows
    in the following table(from [here](http://www.pdmi.ras.ru/~lowdimma/topics_nth/conway_blocks.pdf).

The fouth column in the table says what other
    subsequences the given subsequence evolves into. He also show that the
    number of the digits in each member of the sequence grows a constant from
    one member to the next. If L<ins>n</ins> is the number of the digits in the
    n<sup>th</sup> member in the sequence, then L<ins>n+1</ins>/L<ins>n</ins> to
      a limitation when n to infinity. It is 1.303577269... , which we call it
      as **Conway Constant**.
<p>
  <table style="margin-right: auto; white-space: nowrap; width: auto;">
      <tbody>
        <tr>
          <th>No.</th>
          <th>Subsequence</th>
          <th>Length</th>
          <th>Evolves Into</th>
        </tr>
        <tr>
          <td><strong>1</strong></td>
          <td>1112</td>
          <td>4</td>
          <td>(63)</td>
        </tr>
        <tr>
          <td><strong>2</strong></td>
          <td>1112133</td>
          <td>7</td>
          <td>(64)(62)</td>
        </tr>
        <tr>
          <td><strong>3</strong></td>
          <td>111213322112</td>
          <td>12</td>
          <td>(65)</td>
        </tr>
        <tr>
          <td><strong>4</strong></td>
          <td>111213322113</td>
          <td>12</td>
          <td>(66)</td>
        </tr>
        <tr>
          <td><strong>5</strong></td>
          <td>1113</td>
          <td>4</td>
          <td>(68)</td>
        </tr>
        <tr>
          <td><strong>6</strong></td>
          <td>11131</td>
          <td>5</td>
          <td>(69)</td>
        </tr>
        <tr>
          <td><strong>7</strong></td>
          <td>111311222112</td>
          <td>12</td>
          <td>(84)(55)</td>
        </tr>
        <tr>
          <td><strong>8</strong></td>
          <td>111312</td>
          <td>6</td>
          <td>(70)</td>
        </tr>
        <tr>
          <td><strong>9</strong></td>
          <td>11131221</td>
          <td>8</td>
          <td>(71)</td>
        </tr>
        <tr>
          <td><strong>10</strong></td>
          <td>1113122112</td>
          <td>10</td>
          <td>(76)</td>
        </tr>
        <tr>
          <td><strong>11</strong></td>
          <td>1113122113</td>
          <td>10</td>
          <td>(77)</td>
        </tr>
        <tr>
          <td><strong>12</strong></td>
          <td>11131221131112</td>
          <td>14</td>
          <td>(82)</td>
        </tr>
        <tr>
          <td><strong>13</strong></td>
          <td>111312211312</td>
          <td>12</td>
          <td>(78)</td>
        </tr>
        <tr>
          <td><strong>14</strong></td>
          <td>11131221131211</td>
          <td>14</td>
          <td>(79)</td>
        </tr>
        <tr>
          <td><strong>15</strong></td>
          <td>111312211312113211</td>
          <td>18</td>
          <td>(80)</td>
        </tr>
        <tr>
          <td><strong>16</strong></td>
          <td>111312211312113221133211322112211213322112</td>
          <td>42</td>
          <td>(81)(29)(91)</td>
        </tr>
        <tr>
          <td><strong>17</strong></td>
          <td>111312211312113221133211322112211213322113</td>
          <td>42</td>
          <td>(81)(29)(90)</td>
        </tr>
        <tr>
          <td><strong>18</strong></td>
          <td>11131221131211322113322112</td>
          <td>26</td>
          <td>(81)(30)</td>
        </tr>
        <tr>
          <td><strong>19</strong></td>
          <td>11131221133112</td>
          <td>14</td>
          <td>(75)(29)(92)</td>
        </tr>
        <tr>
          <td><strong>20</strong></td>
          <td>1113122113322113111221131221</td>
          <td>28</td>
          <td>(75)(32)</td>
        </tr>
        <tr>
          <td><strong>21</strong></td>
          <td>11131221222112</td>
          <td>14</td>
          <td>(72)</td>
        </tr>
        <tr>
          <td><strong>22</strong></td>
          <td>111312212221121123222112</td>
          <td>24</td>
          <td>(73)</td>
        </tr>
        <tr>
          <td><strong>23</strong></td>
          <td>111312212221121123222113</td>
          <td>24</td>
          <td>(74)</td>
        </tr>
        <tr>
          <td><strong>24</strong></td>
          <td>11132</td>
          <td>5</td>
          <td>(83)</td>
        </tr>
        <tr>
          <td><strong>25</strong></td>
          <td>1113222</td>
          <td>7</td>
          <td>(86)</td>
        </tr>
        <tr>
          <td><strong>26</strong></td>
          <td>1113222112</td>
          <td>10</td>
          <td>(87)</td>
        </tr>
        <tr>
          <td><strong>27</strong></td>
          <td>1113222113</td>
          <td>10</td>
          <td>(88)</td>
        </tr>
        <tr>
          <td><strong>28</strong></td>
          <td>11133112</td>
          <td>8</td>
          <td>(89)(92)</td>
        </tr>
        <tr>
          <td><strong>29</strong></td>
          <td>12</td>
          <td>2</td>
          <td>(1)</td>
        </tr>
        <tr>
          <td><strong>30</strong></td>
          <td>123222112</td>
          <td>9</td>
          <td>(3)</td>
        </tr>
        <tr>
          <td><strong>31</strong></td>
          <td>123222113</td>
          <td>9</td>
          <td>(4)</td>
        </tr>
        <tr>
          <td><strong>32</strong></td>
          <td>12322211331222113112211</td>
          <td>23</td>
          <td>(2)(61)(29)(85)</td>
        </tr>
        <tr>
          <td><strong>33</strong></td>
          <td>13</td>
          <td>2</td>
          <td>(5)</td>
        </tr>
        <tr>
          <td><strong>34</strong></td>
          <td>131112</td>
          <td>6</td>
          <td>(28)</td>
        </tr>
        <tr>
          <td><strong>35</strong></td>
          <td>13112221133211322112211213322112</td>
          <td>32</td>
          <td>(24)(33)(61)(29)(91)</td>
        </tr>
        <tr>
          <td><strong>36</strong></td>
          <td>13112221133211322112211213322113</td>
          <td>32</td>
          <td>(24)(33)(61)(29)(90)</td>
        </tr>
        <tr>
          <td><strong>37</strong></td>
          <td>13122112</td>
          <td>8</td>
          <td>(7)</td>
        </tr>
        <tr>
          <td><strong>38</strong></td>
          <td>132</td>
          <td>3</td>
          <td>(8)</td>
        </tr>
        <tr>
          <td><strong>39</strong></td>
          <td>13211</td>
          <td>5</td>
          <td>(9)</td>
        </tr>
        <tr>
          <td><strong>40</strong></td>
          <td>132112</td>
          <td>6</td>
          <td>(10)</td>
        </tr>
        <tr>
          <td><strong>41</strong></td>
          <td>1321122112</td>
          <td>10</td>
          <td>(21)</td>
        </tr>
        <tr>
          <td><strong>42</strong></td>
          <td>132112211213322112</td>
          <td>18</td>
          <td>(22)</td>
        </tr>
        <tr>
          <td><strong>43</strong></td>
          <td>132112211213322113</td>
          <td>18</td>
          <td>(23)</td>
        </tr>
        <tr>
          <td><strong>44</strong></td>
          <td>132113</td>
          <td>6</td>
          <td>(11)</td>
        </tr>
        <tr>
          <td><strong>45</strong></td>
          <td>1321131112</td>
          <td>10</td>
          <td>(19)</td>
        </tr>
        <tr>
          <td><strong>46</strong></td>
          <td>13211312</td>
          <td>8</td>
          <td>(12)</td>
        </tr>
        <tr>
          <td><strong>47</strong></td>
          <td>1321132</td>
          <td>7</td>
          <td>(13)</td>
        </tr>
        <tr>
          <td><strong>48</strong></td>
          <td>13211321</td>
          <td>8</td>
          <td>(14)</td>
        </tr>
        <tr>
          <td><strong>49</strong></td>
          <td>132113212221</td>
          <td>12</td>
          <td>(15)</td>
        </tr>
        <tr>
          <td><strong>50</strong></td>
          <td>13211321222113222112</td>
          <td>20</td>
          <td>(18)</td>
        </tr>
        <tr>
          <td><strong>51</strong></td>
          <td>1321132122211322212221121123222112</td>
          <td>34</td>
          <td>(16)</td>
        </tr>
        <tr>
          <td><strong>52</strong></td>
          <td>1321132122211322212221121123222113</td>
          <td>34</td>
          <td>(17)</td>
        </tr>
        <tr>
          <td><strong>53</strong></td>
          <td>13211322211312113211</td>
          <td>20</td>
          <td>(20)</td>
        </tr>
        <tr>
          <td><strong>54</strong></td>
          <td>1321133112</td>
          <td>10</td>
          <td>(6)(61)(29)(92)</td>
        </tr>
        <tr>
          <td><strong>55</strong></td>
          <td>1322112</td>
          <td>7</td>
          <td>(26)</td>
        </tr>
        <tr>
          <td><strong>56</strong></td>
          <td>1322113</td>
          <td>7</td>
          <td>(27)</td>
        </tr>
        <tr>
          <td><strong>57</strong></td>
          <td>13221133112</td>
          <td>11</td>
          <td>(25)(29)(92)</td>
        </tr>
        <tr>
          <td><strong>58</strong></td>
          <td>1322113312211</td>
          <td>13</td>
          <td>(25)(29)(67)</td>
        </tr>
        <tr>
          <td><strong>59</strong></td>
          <td>132211331222113112211</td>
          <td>21</td>
          <td>(25)(29)(85)</td>
        </tr>
        <tr>
          <td><strong>60</strong></td>
          <td>13221133122211332</td>
          <td>17</td>
          <td>(25)(29)(68)(61)(29)(89)</td>
        </tr>
        <tr>
          <td><strong>61</strong></td>
          <td>22</td>
          <td>2</td>
          <td>(61)</td>
        </tr>
        <tr>
          <td><strong>62</strong></td>
          <td>3</td>
          <td>1</td>
          <td>(33)</td>
        </tr>
        <tr>
          <td><strong>63</strong></td>
          <td>3112</td>
          <td>4</td>
          <td>(40)</td>
        </tr>
        <tr>
          <td><strong>64</strong></td>
          <td>3112112</td>
          <td>7</td>
          <td>(41)</td>
        </tr>
        <tr>
          <td><strong>65</strong></td>
          <td>31121123222112</td>
          <td>14</td>
          <td>(42)</td>
        </tr>
        <tr>
          <td><strong>66</strong></td>
          <td>31121123222113</td>
          <td>14</td>
          <td>(43)</td>
        </tr>
        <tr>
          <td><strong>67</strong></td>
          <td>3112221</td>
          <td>7</td>
          <td>(38)(39)</td>
        </tr>
        <tr>
          <td><strong>68</strong></td>
          <td>3113</td>
          <td>4</td>
          <td>(44)</td>
        </tr>
        <tr>
          <td><strong>69</strong></td>
          <td>311311</td>
          <td>6</td>
          <td>(48)</td>
        </tr>
        <tr>
          <td><strong>70</strong></td>
          <td>31131112</td>
          <td>8</td>
          <td>(54)</td>
        </tr>
        <tr>
          <td><strong>71</strong></td>
          <td>3113112211</td>
          <td>10</td>
          <td>(49)</td>
        </tr>
        <tr>
          <td><strong>72</strong></td>
          <td>3113112211322112</td>
          <td>16</td>
          <td>(50)</td>
        </tr>
        <tr>
          <td><strong>73</strong></td>
          <td>3113112211322112211213322112</td>
          <td>28</td>
          <td>(51)</td>
        </tr>
        <tr>
          <td><strong>74</strong></td>
          <td>3113112211322112211213322113</td>
          <td>28</td>
          <td>(52)</td>
        </tr>
        <tr>
          <td><strong>75</strong></td>
          <td>311311222</td>
          <td>9</td>
          <td>(47)(38)</td>
        </tr>
        <tr>
          <td><strong>76</strong></td>
          <td>311311222112</td>
          <td>12</td>
          <td>(47)(55)</td>
        </tr>
        <tr>
          <td><strong>77</strong></td>
          <td>311311222113</td>
          <td>12</td>
          <td>(47)(56)</td>
        </tr>
        <tr>
          <td><strong>78</strong></td>
          <td>3113112221131112</td>
          <td>16</td>
          <td>(47)(57)</td>
        </tr>
        <tr>
          <td><strong>79</strong></td>
          <td>311311222113111221</td>
          <td>18</td>
          <td>(47)(58)</td>
        </tr>
        <tr>
          <td><strong>80</strong></td>
          <td>311311222113111221131221</td>
          <td>24</td>
          <td>(47)(59)</td>
        </tr>
        <tr>
          <td><strong>81</strong></td>
          <td>31131122211311122113222</td>
          <td>23</td>
          <td>(47)(60)</td>
        </tr>
        <tr>
          <td><strong>82</strong></td>
          <td>3113112221133112</td>
          <td>16</td>
          <td>(47)(33)(61)(29)(92)</td>
        </tr>
        <tr>
          <td><strong>83</strong></td>
          <td>311312</td>
          <td>6</td>
          <td>(45)</td>
        </tr>
        <tr>
          <td><strong>84</strong></td>
          <td>31132</td>
          <td>5</td>
          <td>(46)</td>
        </tr>
        <tr>
          <td><strong>85</strong></td>
          <td>311322113212221</td>
          <td>15</td>
          <td>(53)</td>
        </tr>
        <tr>
          <td><strong>86</strong></td>
          <td>311332</td>
          <td>6</td>
          <td>(38)(29)(89)</td>
        </tr>
        <tr>
          <td><strong>87</strong></td>
          <td>3113322112</td>
          <td>10</td>
          <td>(38)(30)</td>
        </tr>
        <tr>
          <td><strong>88</strong></td>
          <td>3113322113</td>
          <td>10</td>
          <td>(38)(31)</td>
        </tr>
        <tr>
          <td><strong>89</strong></td>
          <td>312</td>
          <td>3</td>
          <td>(34)</td>
        </tr>
        <tr>
          <td><strong>90</strong></td>
          <td>312211322212221121123222113</td>
          <td>27</td>
          <td>(36)</td>
        </tr>
        <tr>
          <td><strong>91</strong></td>
          <td>312211322212221121123222122</td>
          <td>27</td>
          <td>(35)</td>
        </tr>
        <tr>
          <td><strong>92</strong></td>
          <td>32112</td>
          <td>5</td>
          <td>(37)</td>
        </tr>
      </tbody>
    </table>
</p>

Those 92 subsequence is so basic that is constructs every member in the look-and-say
    sequence. Just like 92 elements. [Here](http://mathworld.wolfram.com/CosmologicalTheorem.html)
    gives the periodic table of atoms associated with the look-and-say sequence
    as named by Conway(1987). As we can see, 3113112211322112 links to **Br**, and
    311311 links to **Ba**.

**Br**eaking **Ba**d. That is the answer.

## **0x02 More**

That is perfect from the begining to the end. Many thanks to the problem
    maker, and the screenwriters, also every
    excellent actors in Breaking Bad.


[View on GitHub](https://github.com/qiwihui/blog/issues/2)


