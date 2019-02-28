# insect_rasp

### overview ###
This is  a humidity & temperature reader.  It use a sensor named "DHT22" and "Adafruit Python DHT" Sensor Library.

<em>Adafruit Python DHT</em>
<a target="ada_lef" href="https://github.com/adafruit/Adafruit_Python_DHT">https://github.com/adafruit/Adafruit_Python_DHT</a>

### requirements ###
You should install following tools on Raspbian.
<ul>
    <li>Python3</li>
    <li>Adafruit Python DHT Library </li>
    <li>GPIO Library(from pip3)</li>
</ul>

###  setup ###
<ul type="num">
    <li>connect lines</li>
    <li>put subscriber.py to "dafruit Python DHT Library/subs"</li>
</ul>

###  usage ###

<p>python subscriber.py &lt;GPIO&gt; &lt;POST_URL&gt; &lt;interval_second&gt;</p>
<p>python subscriber.py 4 http://localhost/api/pushto 30</p>

<p>now writing...</p>
