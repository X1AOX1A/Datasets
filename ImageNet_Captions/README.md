# imagenet-captions
Release of ImageNet-Captions

The json file contains a list of dictionaries describing the images in the dataset. Each image has the following information:

* filename: str
* wnid: str
* title: str
* description: str
* tags: list of str

Feel free to create your own captions, or just combine title, tag, description separated by spaces.

Paper link: http://arxiv.org/abs/2205.01397

NoCLIP Model link (35.7% ImageNet top-1): https://drive.google.com/file/d/100FHV8q75DLsef1l5_oJsdjIidyjp7RP/view?usp=sharing

- [Download&Ref](https://github.com/mlfoundations/imagenet-captions)

# Examples

```json
{
        "filename": "n03146219_14833.JPEG",
        "title": "ca. 1480-1490 - 'field armour and horse armour', Landshut/South German, Deutsches Historisches Museum, Berlin, Germany",
        "tags": [
            "berlin",
            "berlijn",
            "deutsches",
            "historisches",
            "museum",
            "zeughaus",
            "landshut",
            "field",
            "armour",
            "feldharnisch",
            "armure",
            "rossharnisch",
            "paardenharnas",
            "veldharnas",
            "1470",
            "ca",
            "1480",
            "1490",
            "um",
            "horse",
            "harnois",
            "cheval",
            "schaller",
            "salade",
            "sallet",
            "gauntlet",
            "gantelet",
            "besagew",
            "chamfron",
            "chanfron",
            "barding",
            "rosskopf",
            "harnas",
            "wapenrusting",
            "harnisch",
            "r\u00fcstung"
        ],
        "description": "",
        "wnid": "n03146219"
    },
    {
        "filename": "n03146219_27278.JPEG",
        "title": "cuirasses",
        "tags": [
            "cuirasse",
            "mus\u00e9e-de-la-pr\u00e9histoire",
            "saint-germain-en-laye"
        ],
        "description": "mus\u00e9e des antiquit\u00e9s nationales de Saint Germain en Laye",
        "wnid": "n03146219"
    },
    {
        "filename": "n03146219_25321.JPEG",
        "title": "Armor (Gusoku)",
        "tags": [
            "new york",
            "new york city",
            "nyc",
            "museum",
            "metropolitan museum of art",
            "Art"
        ],
        "description": "Armor (Gusoku)  \nJapan, late Edo period, early to mid-19th century  \n\nThis armor was assembled in the nineteenth century and reflects several waves of Western influence on Japan.  The helmet follows the shape of a late sixteenth-century Dutch Cabasset but is a contemporary copy by the Japanese armorer Saotome Iyeiada, whose signature is found inside the bowl.  The cuirass appears to be of early nineteenth century European manufacture.  These older elements. completed by more modern ones, were decorated with Buddhist divinities and literary figures rendered by a Japanese craftsman using a Western process, etching.  The helmet bears the badge of the Arima family, daimyo of Kuzume.",
        "wnid": "n03146219"
    },
```