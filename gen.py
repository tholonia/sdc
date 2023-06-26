#!/bin/env python
import random
import getopt,sys
import json
import os
from pprint import pprint



#^ define selection arrays


# globalIdx = True
globalIdx = False

xpre = [
    "realistic photograph",
    "artistic painting",
    "cartoon style",
    "polaroid photograph",
    "pen and ink drawing",
    "abstract painting",
    "old black and white photoghraph",
    "crayon drawing"
]

suf = ""

pre = [
    "portrait",
    # f"black and white pen and ink drawing",
 #   f"polaroid photograph",
  #  f"black and white photograph",
   # f"brownie camera photograph"
]

background = [
    "blackness",
    "dark black",
]

places=[
    "forest",
    "jungle",
    "swamp",
    # "desert",
    # "mountain",
    # "lake",
    "valley",
    # "city",
    # "town",
    # "road",
    "outerspace",
    "outer space",
    "river",
    # "war",
    # "slum",
    # "car"
]

adj = ["amazed","aggravated","anxious","attractive","awful","awestruck","bold","chilly","bashful","brave","dejected","cautious","bubbly","dirty","composed","cheerful","dreadful","easygoing","comfortable","heavy","horrified","delightful","irritated","intelligent","excited","pessimistic","numb","festive","tearful","puzzled","free","tense","quizzical","jolly","terrible","ravenous","optimistic","tired","reluctant","proud","ugly","settled","wonderful","weak","shy"]
# adj = ["colorful","pretty"]
verbs = ["arising","beating","betting","biting","bleeding","blowing","building","catching","creeping","cuting","drawing","dreaming","drinking","driving","eating","falling","feeding","fighting","fleeing","flying","freezing","hanging","hiding","hitting","holding","kneeling","leading","meeting","reading","riding","ringing","rising","running","sewing","shaking","shining","shooting","singing","sinking","siting","sleeping","sliding","speaking","spliting","standing","stinging","striking","sweeping","swimming","teaching","tearing","throwing","weaving","weeping","writing"]
# verbs = ["above","below"]

animals=["ground hog","prairie dog","mare","ram","ape","grizzly bear","chipmunk","chameleon","donkey","wildcat","reindeer","pony","aardvark","dromedary","elk","parakeet","canary","impala","turtle","mountain goat","jaguar","iguana","hyena","cheetah","bighorn","basilisk","llama","chimpanzee","toad","alligator","bald eagle","weasel","rooster","colt","wolverine","addax","warthog","panda","chamois","musk-ox","fox","mustang","chinchilla","lion","fish","snowy owl","rhinoceros","silver fox","otter","antelope","guinea pig","budgerigar","puma","waterbuck","polar bear","dugong","wolf","camel","squirrel","parrot","dingo","mule","whale","gazelle","panther","starfish","dog","pig","walrus","duckbill platypus","deer","giraffe","mongoose","argali","newt","raccoon","anteater","kitten","kangaroo","wombat","gemsbok","moose","lamb","dung beetle","peccary","seal","coati","lovebird","opossum","gopher","orangutan","beaver","buffalo","armadillo","hare","vicuna","blue crab","meerkat","springbok","mynah bird","porcupine","lynx","bull","horse","leopard","gila monster","pronghorn","quagga","bison","okapi","tiger","baboon","rat","chicken","snake","guanaco","civet","ewe","koala","doe","ibex","stallion","skunk","fawn","tapir","muskrat","eland","ferret","frog","gnu","jackal","porpoise","oryx","yak","eagle owl","bunny","octopus","elephant","woodchuck","zebra","lizard","marmoset","musk deer","mandrill","badger","crocodile","mink","ox","cat","shrew","hartebeest","salamander","bear","jerboa","hamster","zebu","coyote","alpaca","puppy","sloth","rabbit","goat","hedgehog","burro","mole","aoudad","ocelot","thorny devil","boar","mouse","sheep","finch","dormouse","crow","hog","cougar","monkey","lemur","highland cow","cow","hippopotamus","marten","capybara","steer","ermine","gorilla","bat"]
birds=["Victoria Crowned Pigeon","Hadada Ibis","Roseate Spoonbill","Trumpeter Hornbill","White-headed Wattled Lapwing","Blue-bellied Roller","Green-winged Macaw","Golden-crested Mynah","Bateleur Eagle","Bald Eagle","Sun Conure","Common Grackle","Spectacled Owl","Harris's Hawk","Gouldian Finch","Cattle Egret","Cut-throat Finch","Collared Finch-Billed Bulbul","Melba Finch","Silver Gull","Rainbow Lorikeet","Guam Kingfisher","White-tailed Trogon","Black-faced Tanager","Augur Buzzard","American Crow","White-necked Raven","Andean Condor","Brown Pelican","European Starling","Military Macaw","Golden-breasted Starling","Ringed Teal","Boat-billed Heron","Blue-grey Tanager","Palm Cockatoo","Shaft-tailed Finch","Laughing Kookaburra","Hooded Vulture","Scarlet-headed Blackbird","Violaceous Euphonia","Snowy Owl","White-eared Catbird","Black Vulture","Malayan Great Argus","African Grey Parrot","Burrowing Owl","Keel-billed Toucan","Yellow-naped Amazon","Canary","Blue-crowned Motmot","White-cheeked Turaco","American Flamingo","Sunbittern","Hooded Merganser","Nicobar Pigeon","Black-faced Dacnis","Red-fronted Macaw","Two-toed Sloth","Inca Dove","Eastern Screech Owl","Bali Mynah","Scaly-sided Merganser","Crested Coua","Guam Rail","Smew","Blue-fronted Amazon Parrot","Indian Runner Duck","Snowy Egret","Taveta Golden Weaver","Bridled White-eye","Wattled Curassow","Green-naped Pheasant Pigeon","Scarlet Macaw","Bearded Barbet","Sudan Golden Sparrow","Black-naped Fruit Dove","African Pygmy Falcon","Eurasian Eagle-Owl","Malayan Flying Fox","Inca Tern","Black Kite","Lanner Falcon","Green Singing Finch","Martial Eagle","White-throated Ground Dove","White-crested Laughing Thrush","Pied Imperial Pigeon","Purple-throated Fruit Crow","Scarlet Ibis","Scissor-tailed Flycatcher","Spangled Cotinga","Pekin Robin","Giant Cowbird","Dhyal Thrush","Greater Roadrunner","Ruddy Duck","Red-tailed Hawk","Black-headed Gonolek","Fairy Bluebird","Raggiana Bird-of-Paradise","Guira Cuckoo","Meyer's Parrot","Palm Tanager","Orange Bishop","Palawan Peacock-pheasant","Curl-crested Aracari","White-bellied Go-away-bird","Red Bishop Weaver","Green Woodhoopoe","Hamerkop","Green Aracari","Crested Wood Partridge","West Indian Whistling Duck","Southern Ground Hornbill","African Penguin","Rosybill Pochard","Troupial","Hyacinth Macaw","Brazilian Tanager","Paradise Whydah","Golden Conure","Red-legged Honeycreeper","Grey-winged Trumpeter","Rhinoceros Hornbill","Steller's Sea Eagle","Screaming Piha","Call Duck","Grosbeak Starling","Crested Oropendola","Southern Bald Ibis","Yellow-hooded Blackbird","Javan Pond Heron","American Kestrel"]
clothes=["Scarf","Cargos","Poncho","Blouse","Dress","Pajamas","Tie","Suit","Gown","Jeans","Tights","Fleece","Polo Shirt","Swimwear","Thong","Corset","Boxers","Coat","Knickers","Sunglasses","Hoody","Gloves","Top","Skirt","Slippers","Bikini","Sandals","Socks","Shirt","Briefs","Belt","Sarong","Shawl","Kilt","Tankini","Bow Tie","Cufflinks","Sweatshirt","Cardigan","T-Shirt","Hat","Robe","Stockings","Blazer","Shoes","Tracksuit","Jogging Suit","Nightgown","Shorts","Lingerie","Jacket","Dinner Jacket","Waistcoat","Swimming Shorts","Cummerbund","Boots","Overalls","Underwear","Camisole","Bra","Cravat"]
fish=["triggerfish","scorpion fish","boxfish","bonito","butterflyfish","stonefish","clownfish","yellowfin tuna","angel fish","squirrelfish","skate","oyster toadfish","wahoo","speckled hind","scup","ocean sunfish","speckled trout","gray trout","tiger shark","batfish","mako shark","paddlefish","mandarin fish","amberjack","cusk","sea mullet","basselets","oarfish","sailfish","starfish","wolffish","albacore","mackerel","hickory shad","little tunny","flounder","needlefish","white grunt","surgeonfish","barracuda","vermillion snapper","sheepshead","scamp","striped bass","banded sea krait","king mackerel","goatfish","blueline tilefish","knobbed porgy","blacktip shark","lizardfish","pinfish","blobfish","pollock","bank sea bass","blackfin tuna","hogfish","salmon","whale shark","butterfish","croaker","cleaner fish","gnomefish","red drum","pigfish","drums","spanish mackerel","dolphin","gag grouper","alligator gar","swordfish","gray triggerfish","stingrays","bluefin tuna","bigeye tuna","spottail pinfish","spot","parrotfish","catfish","skipjack tuna","smelt","searobin","seahorse","plecostomus","cardinalfish","northern puffer","pompano","pufferfish","snapper","halibut","yellowedge grouper","bluefish","weakfish","puffers","silver snapper","unicornfish","damselfish","menhaden","hawkfish","flatfish","silver perch","tarpon","cobia","red snapper","black sea bass","cod","stingray","yellowtail snapper","black drum","flying fish","grouper","haddock","white marlin","rabbitfish","hammerhead","jumping mullet","red grouper","tautog","blue marlin","atlantic bonito","payara","spadefish"]
flowers=["Loosestrife","Astilbe","Oleander","Snowdrops","Balloon Flower","Narcissus","Cosmos","Bellflower","Clematis","Larkspur","Geranium","Kerria","Rose of Sharon","Artemisia","Lobelia","Lavender","Anemone","Hosta","Trumpet Vine","Jupiter’s Beard","Crocus","Catmint","Silver Lace Vine","Marigold","Mock Orange","Lily-of-the-Valley","Hyacinth","Sedum","Butterfly Weed","Hardy Geranium","Blanketflower","Wisteria","Impatien","Hollyhock","New Guinea impatien","Lilac","Peony","Coneflower","Passion Flower","Lupine","Tulip","Shrub Roses","Chrysanthemum","Pansy","Bee Balm","Nicotiana","Vinca","Yarrow","Salvia","Dahlia","Lamium","Scilla","Gas Plant","Snap Dragon","Camellia","Morning Glory","Bougainvillea","Foxglove","Alyssum","Shasta Daisy","Sweet Pea","Bleeding Heart","Coral Bells","Aster","Columbine","Gladiolus","Poppy","Allium","Bachelor Button","Primrose","Petunias","Day Lily","Hybrid Tea Roses","Butterfly Bush","Broom","Iris","Globeflower","Moon Flower","Scabiosa","Coreopsis","Hydrangea","Nasturtium","Rhododendron","Grape Hyacinth","Cyclamen","Delphinium","Pinks","Gayfeather","Honeysuckle","Lantana","Snowball bush"]
trees=["pine tree","oak tree", "birch tree", "maple tree"]
instruments=["Steel Pan","Wooden Flute","Guitar","Clarinet","Trumpet","Whistle","Ukulele","Cowbell","Piccolo","Acoustic Guitar","French Horn","Bongos","Slide Whistle","Bass Guitar","Oboe","Fiddle","Steel Drums","Bagpipes","Violin","Triangle","Xylophone","Kazoo","Maracas","Organ","Shakers","Zither","Ocarina","Harmonica","Drums","Saxophone","Symbols","Recorder","Tambourine","Spoons","Turntables","Voice","Vibraphone","Trombone","Harp","Bells","Snare Drum","Vocals","Crystal Glasses","Tuba","Flute","Viola","Keyboard","Bamboo Flute","Accordion","Piano","Banjo"]
snakes=["Viper","Twig Snake","Rattlesnake","Philippine Cobra","Burrowing asp","Corn Snake","Horned Viper","Taipan","Black Mamba","Common Garter Snake","Mexican Jumping Viper","Coral cobra","Langaha Nasuta","Black Racer","Blue Krait","Spiny Tree Viper","Tiger Keelback","Eastern Brown Snake","Golden Lancehead","Ball Python","Mamushi","California King Snake","Hognosed Pitviper","Death Adder","Ringneck snake","Elephant Trunk Snake","Tiger Snake","Water Cobra","Sea Snake","Inland Taipan","Long Nosed Vine Snake","Boa Constrictor","Milk Snake","Flying Snake","Atheris Hispida","Tentacled Snake","Fierce Snake"]
things=["boom box","deodorant","shoes","sun glasses","playing card","twezzers","bookmark","sofa","computer","wallet","headphones","stop sign","teddies","shirt","button","bread","watch","thermometer","television","perfume","greeting card","bag","socks","door","toothpaste","vase","drill press","hair brush","pen","knife","needle","tire swing","tomato","fork","bracelet","credit card","tissue box","desk","clamp","screw","mp3 player","sand paper","air freshener","candy wrapper","soy sauce packet","outlet","conditioner","balloon","food","scotch tape","paper","bananas","shampoo","buckle","rubber band","lamp shade","glass","lace","twister","helmet","toe ring","monitor","model car","milk","pillow","stockings","leg warmers","drawer","flag","rubber duck","box","toothbrush","white out","clothes","soap","eye liner","mop","sticky note","checkbook","cookie jar","cinder block","camera","tooth picks","chapter book","puddle","brocolli","speakers","bow","glasses","candle","seat belt","sidewalk","plate","rug","pool stick","glow stick","chair","shawl","cell phone","bottle","hair tie","photo album","newspaper","fake flowers","paint brush","sponge","carrots","table","tv","lip gloss","rusty nail","lamp","blanket","spring","slipper","thread","lotion","bowl","sketch pad","cup","sandal","packing peanuts","plastic fork","keyboard","hanger","doll","keys","USB drive","pencil","beef","floor","eraser","clay pot","purse","CD","cat","radio","nail file","coasters","nail clippers","house","grid paper","water bottle","bottle cap","window","thermostat","soda can","apple","face wash","phone","cork","towel","chalk","ring","key chain","shovel","flowers","book","controller","pants","bed","ice cube tray","remote","sharpie","street lights","canvas","mouse pad","toilet","wagon","washing machine","charger","shoe lace","spoon","picture frame","money","video games","ipod","blouse","mirror","zipper","car","couch","truck","chocolate","sailboat","magnet","tree","clock","piano","fridge"]
insects=["beetle","ant","ladybug","honey bee","dragonfly","butterfly","scorpion"]

biology = ["atom","molecule","animal cell","virus","bacteria","protazoa","fungus","spores","mushrooms","insects","worms","seeds","ferns","plants","flowers"]

# all = birds+clothes+fish+flowers+instruments+snakes+things
all = fish
# all = biology

models = [
    "deliberate_v2.safetensors [9aba26abdf]",
    # "dreamlike-photoreal-2.0.ckpt [fc52756a74]",
    # "f222.ckpt [9e2c6ceff3]",
    # "modelshoot-1.0.safetensors [80dc271195]",
    # "openjourney-v4.ckpt [02e37aad9f]",  #backwards?
    # "Protogen_V2.2.ckpt [bb725eaf2e]",   #backwards?
    # "sd-v1-4.ckpt [fe4efff1e1]",
    # "v1-5-pruned-emaonly.safetensors [6ce0161689]",

    # "abyssorangemix3AOM3_aom3a1b.safetensors [5493a0ec49]",
    # "anythingV3_fp16.ckpt [812cd9f9d9]",
    # "chilloutmix_NiPrunedFp32Fix.safetensors [fc2511737a]",
    # "dreamshaper_5BakedVae.safetensors [a60cfaa90d]",
        # "elldrethsRetroMix_v10.safetensors [57285e7bd5]",
        # "ghostmix_v20Bakedvae.safetensors [e3edb8a26f]",
        # "meinamix_meinaV9.safetensors [eac6c08a19]",
    # "realisticVisionV20_v20.safetensors [c0d1994c73]",

    # "HassanBlend1.4_Safe.safetensors [b08fdba169]",

]

sampler = [
    # "DDIM"
    "Euler a",
    # "Euler",
    # "DPM2 a",
    # "DPM++ 2S a",
    # "DPM++ 2M",
    # "DPM++ SDE",#lots of BG noise
    # "DPM fast",
    # "DPM adaptive",
    # "LMS Karras",
    # "DPM2 Karras",
    # "DPM++ 2S a Karras",
    # "DPM++ 2M Karras",


    # "DPM++ SDE Karras",

    # "DDIM",
    # "LMS",
    # "DPM2",
    # "Heun",
    # "DPM2 a Karras",
]

#^ define finctions

def r(a,**kwargs):
    try:
        lastr = kwargs['lastr']
    except:
        lastr = False
    try:
        idx = kwargs['idx']
    except:
        idx = False

    if globalIdx:
        rv = a[idx % len(a)]
        return rv
    else:
        rv = random.choice(a)
        if rv == lastr:
            rv = r(a,lastr=lastr)
        return rv
def showhelp():
    print("help")
    rs = '''
    -h, --help          show help
    -c, --count         # prompt items
    -m  --mult          frame multiplier
    -m  --time          lentg in minutes
    -l, --label         label
'''
    print(rs)

#[ MAIN ]

count = 10
mult = 10
runtime = 1.0
lines = False
showkey = False
fps=15
fromfile = "/home/jw/src/sdw/rando_settings.txt"

lastr = False
lastc = False

lastpre =  False
lastadj = False
lastverbs =  False
lastall0=  False
lastall1=  False
lastplaces =  False
lastbg =  False

commandline = ' '.join(sys.argv)

argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv, "hc:m:t:f:s:", [
        "help",
        "count=",
        "mult=",
        "time=",
        "from=",
        "show=",
    ])
except Exception as e:
    print(str(e))
for opt, arg in opts:
    if opt in ("-h", "--help"):
        showhelp()
    if opt in ("-c", "--count"):
        count=int(arg)
    if opt in ("-m", "--mult"):
        mult=int(arg)
    if opt in ("-f", "--from"):
        fromfile=arg
    if opt in ("-s", "--show"):
        showkey=arg
    if opt in ("-t", "--time"):
        runtime=float(arg)
        if lines:
            totframes = int(fps*(runtime*60))
        else:
            totframes = count * mult
        print(f"TOTAL FRAMES: {totframes}", file=sys.stderr)

#^ load original template into JSON array
f = open(fromfile)
aorg = json.load(f)

#- make prompts
aprompts = {}
for i in range(count):
    newpre = r(pre,lastr=lastpre,idx=i)
    newadj = r(adj,lastr=lastadj,idx=i)
    newall0 = r(all,lastr=lastall0,idx=i)
    newall1 = r(all,lastr=lastall1,idx=i)
    newverbs = r(verbs,lastr=lastverbs,idx=i)
    newplaces = r(places,lastr=lastplaces,idx=i)
    newbg = r(background,lastr=lastbg,idx=i)

    #aprompts[i * mult] = f"{newpre} of a {newadj} {newall0} {newverbs} a {newall1} in a {newplaces}, background of a vibrant {newbg}"
    aprompts[i * mult] = f"{newpre} of a {newall0}"

    lastpre = newpre
    lastadj = newadj
    lastverbs = newverbs
    lastall0 = newall0
    lastall1 = newall1
    lastplaces = newplaces
    lastbg = newbg

aorg['prompts']=aprompts



#- make models
line = ""
for i in range(count):
    newr = r(models,lastr=lastr,idx=i)
    line = line + f"{i * mult}: (\"{newr}\"),"
    if i == count-1:
        line = line.strip(",")
    lastr=newr
aorg['checkpoint_schedule']=line

#- make samplers
line = ""
for i in range(count):
    newr = r(sampler,lastr=lastr,idx=i)
    # print(newr,lastr,file=sys.stderr)
    line = line + f"{i * mult}: (\"{newr}\")),"
    if i == count-1:
        line = line.strip(",")
    lastr=newr
aorg['sampler_schedule']=line

#[  here is where we set other vars ]

ttime = (count*mult*5) + (count*5)
print(f"TOTAL RUN TIME: {ttime/60}",file=sys.stderr)

aorg['commandline'] = commandline
aorg["max_frames"]=mult*count
# aorg["translation_x"] = "0: (0)"
# aorg["seed"] = -1
# aorg["batch_name"] = "batch3"
# aorg["diffusion_cadence"]=4
# aorg["fps"]=60
# aorg["animation_prompts_positive"] = ""
# aorg["animation_prompts_negative"] = "nsfw, nude, human, man, woman, boy, girl, hands, face",

#^ rotation 1
rot1 = False
if rot1:

    aorg["translation_x"] = "0:(2.5)",
    aorg["translation_y"] = "0: (0)",
    aorg["translation_z"] = "0:((0.125*(cos(120/15*3.141*t/30))+0.0))",
    aorg["transform_center_x"] = "0: (0.5)",
    aorg["transform_center_y"] = "0: (0.5)",
    aorg["rotation_3d_x"] = "0: (0)",
    aorg["rotation_3d_y"] = "0:(-0.5)",
    aorg["rotation_3d_z"] = "0: (0)",


pgen = json.dumps(aorg, indent=4)
print(pgen)

if showkey:
    keys = showkey.split(",")
    for key in keys:
        print("xx--------------------------------------------------------",file=sys.stderr)
        pgen = json.dumps(aorg[key], indent=4)
        if key == "sampler_schedule":
            items = pgen.split(",")
            for item in items:
                print(item,file=sys.stderr)
        else:
            print(pgen,file=sys.stderr)