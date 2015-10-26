script.pulsar.eztv
==================

EZTV Provider for Pulsar

Download it here: https://github.com/platbr/script.pulsar.eztv/releases

Changelog 0.0.9
* Cache system fixed
 * I had forgot to finish the update of cache system.

Changelog 0.0.8
* New cache system
 * Much faster because it uses python's shelve module to store objets and use Threads for background update.
 * Using https://eztv.it again because ez-tv.in has problems, please change the URL.

Changelog 0.0.7
* Using http://ez-tv.in instead of http://eztv.it

Changelog 0.0.6
* Working with Pulsar 0.2
 
Changelog 0.0.5
* Fix a bug in the cache system.

Changelog 0.0.4

Now it has better cache system:
* The second search will be much faster for the same Season, so it can avoid problems with Pulsar timeout (2s).

Now it has interface for configure it:
* URL of EZTV: 
    * You can change it if you need.
* Use Fuzzy
    * Once EZTV does not have a way to search using tvdb_id or imdb_id, we need to use the TV Show name, when the direct comparation between Pulsar provided name and EZTV name fails, we can use Fuzzy Logic to fix it.
* Fuzzy Threshold
    * Control tolerance when using Fuzzy.
* Use Cache for TV Shows List
    * Helps to reduce execution time for every search, once each search need to determine the correspondent eztv show id, before get episodes list.
* Cache TV Shows Timeout (hours)
    * Maximum age.
* Use Cache for Episodes List
    * Helps reduce execution time for sequential searches for the same Season, it avoid to reach Pulsar timeout.
* Cache Episodes Timeout (hours)
    * Maximum age.
![captura de tela 2014-09-19 as 12 36 20](https://cloud.githubusercontent.com/assets/4853326/4338176/4f81230c-4016-11e4-97b9-58a6c508ba67.png)
