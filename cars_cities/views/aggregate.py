from os.path import join
from os import path
from django.views.generic import View
from django.conf import settings
from django.shortcuts import render

from ..models import City
from ..utils.files import pickle_save, pickle_load
from ..utils.shapefile import Reader
import random
import operator


class AggregateStats(View):

    def get(self, request):
        field = request.GET.get('field', 'car_price_avg')
        make = request.GET.get('make')
        model = request.GET.get('model')
        country = request.GET.get('country')
        cities = pickle_load(join(settings.STATS_DIR, 'aggregate'))
        green = pickle_load(join(settings.STATS_DIR, 'city_green'))
        state_data = pickle_load(join(settings.STATS_DIR, 'state_data'))

        green_total = pickle_load(join(settings.STATS_DIR, 'green_total.p'))
        green_trans = pickle_load(join(settings.STATS_DIR, 'green_trans.p'))

        # badList = [115, 117, 121, 122, 128, 129, 132, 135, 144, 160, 167, 173, 183, 192, 195, 197, 203, 212, 226, 229, 234, 258, 266, 276, 278]
        badList = []


        if field == 'actual' or field == 'predicted':
            variable = request.GET.get('variable', 3)
            demog = pickle_load(path.join(settings.STATS_DIR, 'demog'))
            

        for city_id, data in cities.items():
            #print city_id
            if make:
                data['value'] = data.get('makes', {}).get(
                    make, 0) / float(data['total_cars'])
            elif model:
                data['value'] = data.get('models', {}).get(
                    model, 0) / float(data['total_cars'])
            elif country:
                data['value'] = data.get('countries', {}).get(
                    country, 0) / float(data['total_cars'])
            elif field == 'green_gt':
                if city_id not in green:
                    if city_id not in badList:
                        badList.append(city_id)
                else:

                    data['value'] = green[city_id]
            elif field == 'car_mpg_highway_avg':
                if city_id not in green:
                    if city_id not in badList:
                        badList.append(city_id)
                else:

                    data['value'] = data[field]
            elif field == "state_data" or field == "state_gt":
                pass
            elif field == 'actual' or field == 'predicted':
                if city_id not in demog['city_data']:
                    if city_id not in badList:
                        badList.append(city_id)
                else:
                    if field == 'actual':
                        data['value'] = demog['city_data'][city_id]['census'][variable]
                    elif field == 'predicted':
                        data['value'] = demog['city_data'][city_id]['preds'][variable]

            elif field == "rainbow":
                pass
            else:
                data['value'] = data[field]
        


            

        if field:
            for cityID in badList:
                del cities[cityID]
        context = {}


       # if field == "state_data" or field == "state_gt":
        cities_state = state_data
        for city_id, data in cities_state.items():
            if field == "state_data":
                data["value"] = data["data"]
            elif field == "state_gt":
                data["value"] = data["gt"]

        green = green_trans
        # print green_trans
       # if field == "state_data" or field == "state_gt":
        cities_state = state_data
        for city_id, data in cities_state.items():

            state_name = city_id.lower().replace(' ', '')
            if state_name == 'connecticut':
                state_name = 'conneticut'
            if state_name == 'massachusetts':
                state_name = 'massachussetts'
            if state_name == 'pennsylvania':
                state_name = 'pennsilvania'
            if state_name ==    'districtofcolumbia':
                state_name = 'dc'
            if field == "state_data":
                # data["value"] = data["data"]
                if state_name in green:
                    data["value"]  = green[state_name]['data2']
                else:
                    print state_name
            elif field == "state_gt":
                data["value"]  = green[state_name]['gt']
               
            elif field == "rainbow":
                data["value"] = -1
                if city_id == 'Mississippi':
                    data["value"] = 3.660
                if city_id == 'Oklahoma':
                    data["value"] = 7.065

                if city_id == 'Wyoming':
                    data["value"] = 6.296
                if city_id == 'Minnesota':
                    data["value"] = 8.570

                if city_id == 'Illinois':
                    data["value"] = 7.831

                if city_id == 'Arkansas':
                    data["value"] = 5.503

                if city_id == 'New Mexico':
                    data["value"] = 7.969

                if city_id == 'Ohio':
                    data["value"] = 7.579

                if city_id == 'Indiana':
                    data["value"] = 7.297
                if city_id == 'Maryland':
                    data["value"] = 7.303
                if city_id == 'Louisiana':
                    data["value"] = 6.887

                if city_id == 'Idaho':
                    data["value"] = 6.982

                if city_id == 'Arizona':
                    data["value"] = 7.243

                if city_id == 'Iowa':
                    data["value"] = 7.580

                if city_id == 'New York':
                    data["value"] = 7.496

                if city_id == 'Michigan':
                    data["value"] = 7.486

                if city_id == 'Kansas':
                    data["value"] = 7.461

                if city_id == 'Utah':
                    data["value"] = 7.453

                if city_id == 'Virginia':
                    data["value"] = 6.906

                if city_id == 'Oregon':
                    data["value"] = 10.631
                if city_id == 'Connecticut':
                    data["value"] = 7.625
                if city_id == 'Montana':
                    data["value"] = 7.769
                if city_id == 'California':
                    data["value"] = 8.958
                if city_id == 'Massachusetts':
                    data["value"] = 9.580
                if city_id == 'West Virginia':
                    data["value"] = 6.311
                if city_id == 'South Carolina':
                    data["value"] = 5.083
                if city_id == 'New Hampshire':
                    data["value"] = 10.115

                if city_id == 'Vermont':
                    data["value"] = 9.693

                if city_id == 'Georgia':
                    data["value"] = 5.186


                if city_id == 'North Dakota':
                    data["value"] = 6.912
                if city_id == 'Pennsylvania':
                    data["value"] = 7.711

                if city_id == 'Florida':
                    data["value"] = 6.439
                if city_id == 'Alaska':
                    data["value"] = 7.840

                if city_id == 'Kentucky':
                    data["value"] = 7.170
                if city_id == 'Hawaii':
                    data["value"] = 6.982
                if city_id == 'Nebraska':
                    data["value"] = 7.261
                if city_id == 'Missouri':
                    data["value"] = 7.560
                if city_id == 'Wisconsin':
                    data["value"] = 9.106
                if city_id == 'Alabama':
                    data["value"] = 4.343
                if city_id == 'Rhode Island':
                    data["value"] = 8.567
                if city_id == 'South Dakota':
                    data["value"] = 8.514
                if city_id == 'Colorado':
                    data["value"] = 8.826
                if city_id == 'New Jersey':
                    data["value"] = 7.080
                if city_id == 'Washington':
                    data["value"] = 9.958
                if city_id == 'North Carolina':
                    data["value"] = 6.600
                if city_id == 'Tennessee':
                    data["value"] = 5.998
                if city_id == 'District of Columbia':
                    data["value"] = 7.927
                if city_id == 'Texas':
                    data["value"] = 6.522
                if city_id == 'Nevada':
                    data["value"] = 8.247
                if city_id == 'Delaware':
                    data["value"] = 7.378
                if city_id == 'Maine':
                    data["value"] = 8.191
            else:
                data["value"] = 0
                if city_id == 'Mississippi':
                    data["value"] = 3
                if city_id == 'Oklahoma':
                    data["value"] = 1

                if city_id == 'Wyoming':
                    data["value"] = 2
                if city_id == 'Minnesota':
                    data["value"] = 2

                if city_id == 'Illinois':
                    data["value"] = 2

                if city_id == 'Arkansas':
                    data["value"] = 2

                if city_id == 'New Mexico':
                    data["value"] = 2

                if city_id == 'Ohio':
                    data["value"] = 2

                if city_id == 'Indiana':
                    data["value"] = 3
                if city_id == 'Maryland':
                    data["value"] = 2
                if city_id == 'Louisiana':
                    data["value"] = 1

                if city_id == 'Idaho':
                    data["value"] = 3

                if city_id == 'Arizona':
                    data["value"] = 4

                if city_id == 'Iowa':
                    data["value"] = 4

                if city_id == 'New York':
                    data["value"] = 2

                if city_id == 'Michigan':
                    data["value"] = 4

                if city_id == 'Kansas':
                    data["value"] = 4

                if city_id == 'Utah':
                    data["value"] = 1

                if city_id == 'Virginia':
                    data["value"] = 3

                if city_id == 'Oregon':
                    data["value"] = 4
                if city_id == 'Connecticut':
                    data["value"] = 3
                if city_id == 'Montana':
                    data["value"] = 1
                if city_id == 'California':
                    data["value"] = 3
                if city_id == 'Massachusetts':
                    data["value"] = 4
                if city_id == 'West Virginia':
                    data["value"] = 4
                if city_id == 'South Carolina':
                    data["value"] = 3
                if city_id == 'New Hampshire':
                    data["value"] = 1

                if city_id == 'Vermont':
                    data["value"] = 3

                if city_id == 'Georgia':
                    data["value"] = 1


                if city_id == 'North Dakota':
                    data["value"] = 4
                if city_id == 'Pennsylvania':
                    data["value"] = 1

                if city_id == 'Florida':
                    data["value"] = 4
                if city_id == 'Alaska':
                    data["value"] = 0

                if city_id == 'Kentucky':
                    data["value"] = 1
                if city_id == 'Hawaii':
                    data["value"] = 0
                if city_id == 'Nebraska':
                    data["value"] = 1
                if city_id == 'Missouri':
                    data["value"] = 3
                if city_id == 'Wisconsin':
                    data["value"] = 1
                if city_id == 'Alabama':
                    data["value"] = 2
                if city_id == 'Rhode Island':
                    data["value"] = 2
                if city_id == 'South Dakota':
                    data["value"] = 3
                if city_id == 'Colorado':
                    data["value"] = 3
                if city_id == 'New Jersey':
                    data["value"] = 4
                if city_id == 'Washington':
                    data["value"] = 2
                if city_id == 'North Carolina':
                    data["value"] = 2
                if city_id == 'Tennessee':
                    data["value"] = 4
                if city_id == 'District of Columbia':
                    data["value"] = 0
                if city_id == 'Texas':
                    data["value"] = 4
                if city_id == 'Nevada':
                    data["value"] = 2
                if city_id == 'Delaware':
                    data["value"] = 3
                if city_id == 'Maine':
                    data["value"] = 2

                # if city_id == 1:
                #     data["value"] = 5
        if field == "state_data" or field == "state_gt":
            cities_state =self.rank_state(cities_state, field)

        #print settings.LATLNGS_SHP_DIR
        shape = Reader(path.join(settings.LATLNGS_SHP_DIR, 'states'))
        #for sr in shape.shapeRecords():

        # print cities_state
        state_all = {}
        for sr in shape.shapeRecords():

            # print sr.record
            #print sr.record

            if sr.record[0] in cities_state:
            
                state_value = cities_state[sr.record[0]]['value']
                state_all[sr.record[0]] = {}
                

                killPoint = -1 
                for i in range(10, len(sr.shape.points)):
                    if sr.shape.points[i][0] == sr.shape.points[0][0] and sr.shape.points[i][1] == sr.shape.points[0][1]:
                        killPoint = i
                #print len(sr.shape.points)
                if killPoint == -1:
                    killPoint = len(sr.shape.points) - 1
                if sr.record[1] == 50:
                    #print sr.shape.points
                    sr.shape.points= [[-86.83482927725902, 41.765504366361895], [-86.6175922770567, 41.907448366494094], [-86.4988332769461, 42.126446366698055], [-86.3742782768301, 42.249421366812584], [-86.28498027674694, 42.42232436697361], [-86.21785427668442, 42.7748253673019], [-86.27383727673656, 43.12104536762435], [-86.46320127691291, 43.475166367954145], [-86.54130127698565, 43.66318736812926], [-86.44781127689858, 43.772665368231216], [-86.4043452768581, 43.766642368225604], [-86.43410127688581, 43.7814583682394], [-86.42881427688089, 43.82012336827542], [-86.45954827690952, 43.95018436839654], [-86.43814727688958, 43.94559236839227], [-86.51860227696451, 44.053619368492875], [-86.38642327684141, 44.18320436861356], [-86.2719542767348, 44.351228368770045], [-86.23803827670322, 44.52227336892934], [-86.2586272767224, 44.70073136909554], [-86.10848427658256, 44.73444236912694], [-86.08291827655874, 44.77792936916744], [-86.09796427657277, 44.85061236923513], [-86.06745427654435, 44.898257369279506], [-85.79575627629131, 44.9859743693612], [-85.61021527611851, 45.19652736955729], [-85.56551427607688, 45.18056036954242], [-85.65300627615837, 44.95836236933548], [-85.63803927614443, 44.77843536916791], [-85.52608127604016, 44.76316236915369], [-85.45135127597055, 44.860540369244376], [-85.38486927590864, 45.010603369384135], [-85.39024427591364, 45.21159336957132], [-85.37325327589782, 45.273541369629015], [-85.3054752758347, 45.32038336967264], [-85.09286227563669, 45.37022536971906], [-84.98589327553707, 45.37317836972181], [-84.92167427547726, 45.409899369756005], [-85.0818152756264, 45.464650369807], [-85.12044727566237, 45.56977936990491], [-85.07801927562286, 45.63018536996117], [-84.98341227553476, 45.68371337001102], [-84.97203827552416, 45.73774537006133], [-84.72418627529333, 45.78030437010098], [-84.4652752750522, 45.653637369983], [-84.32145827491826, 45.665607369994156], [-84.20556027481032, 45.63090536996184], [-84.13522927474482, 45.57134336990636], [-84.10590727471751, 45.498749369838755], [-83.92289227454707, 45.49177336983226], [-83.7828092744166, 45.40944936975559], [-83.71231827435096, 45.41239436975833], [-83.59236327423923, 45.34950236969976], [-83.49583227414934, 45.360802369710285], [-83.48959827414353, 45.3289373696806], [-83.39401927405451, 45.27290736962843], [-83.42076127407942, 45.25718236961378], [-83.39869527405887, 45.213641369573224], [-83.31270727397879, 45.098620369466104], [-83.44444127410148, 45.052773369423406], [-83.43397227409173, 45.01112836938462], [-83.46490327412053, 44.99788336937229], [-83.42935527408743, 44.926297369305615], [-83.31972427398533, 44.86064636924448], [-83.28081227394908, 44.70318336909783], [-83.32003627398562, 44.515460368922994], [-83.35696327402, 44.33513336875505], [-83.52915027418037, 44.261274368686266], [-83.56823727421677, 44.17011836860137], [-83.59840427424487, 44.07049336850859], [-83.70480227434396, 43.99716536844029], [-83.87361527450118, 43.96284236840833], [-83.91837627454287, 43.916997368365635], [-83.93812127456125, 43.69828336816194], [-83.6991642743387, 43.59964236807008], [-83.65461527429721, 43.607420368077314], [-83.53090927418201, 43.7259433681877], [-83.49424827414786, 43.70284136816619], [-83.46640827412193, 43.74574036820614], [-83.36716327402951, 43.84445236829807], [-83.32602627399119, 43.94045936838749], [-82.94015427363182, 44.069959368508094], [-82.80597827350687, 44.033564368474195], [-82.72790227343415, 43.97250636841733], [-82.61848727333225, 43.787866368245375], [-82.60573827332037, 43.694568368158485], [-82.50382027322546, 43.17225336767204], [-82.41983627314724, 42.97246536748597], [-82.47195227319578, 42.89868236741725], [-82.47323827319697, 42.76289636729079], [-82.51817927323883, 42.634052367170796], [-82.64587727335775, 42.631728367168634], [-82.6340152733467, 42.6693823672037], [-82.72980627343593, 42.681226367214734], [-82.8204072735203, 42.63579436717242], [-82.8023612735035, 42.61292636715112], [-82.88813827358338, 42.495756367042], [-82.87490727357105, 42.458067367006905], [-82.9293892736218, 42.3630403669184], [-83.10758827378775, 42.29270536685289], [-83.19387327386812, 42.11574936668809], [-83.19006627386457, 42.03397936661194], [-83.4826912741371, 41.725130366324294], [-83.76395427439904, 41.71704236631676], [-83.86863927449654, 41.715993366315786], [-84.35920827495342, 41.708039366308384], [-84.38439327497687, 41.70715036630755], [-84.79037727535497, 41.69749436629856], [-84.78847827535321, 41.76095936635767], [-84.82600827538816, 41.761875366358524], [-85.19314027573007, 41.762867366359444], [-85.297209275827, 41.763581366360114], [-85.65945927616437, 41.76262736635922], [-85.79922727629454, 41.76353536636007], [-86.06830227654514, 41.76462836636108], [-86.23456527669998, 41.76486436636131], [-86.52518127697064, 41.76554036636193], [-86.83482927725902, 41.765504366361895]]
                    state_all[sr.record[0]]['polygon'] = map(lambda x: list(x[::-1]), sr.shape.points)
                    state_all[sr.record[0]]['demog'] = state_value

                    sr.shape.points= [[-85.859844276351, 45.969469370277146], [-85.91495527640232, 45.957978370266446], [-85.91710427640432, 45.91819237022939], [-86.06789127654476, 45.964210370272255], [-86.25931927672303, 45.94692937025616], [-86.31563827677549, 45.90568237021774], [-86.34379527680171, 45.83439637015135], [-86.45827527690832, 45.762747370084625], [-86.52939027697455, 45.74896137007178], [-86.52201027696769, 45.724094370048626], [-86.57612427701808, 45.71017437003566], [-86.62978427706805, 45.621233369952826], [-86.68505327711954, 45.650048369979665], [-86.69691927713058, 45.69251137001921], [-86.5847352770261, 45.81387937013224], [-86.7614692771907, 45.82606737014359], [-86.90162427732123, 45.71477837003995], [-87.12375927752811, 45.69624637002269], [-87.26070727765565, 45.55480236989096], [-87.33222727772225, 45.42394236976909], [-87.58386427795662, 45.16273336952582], [-87.59251427796467, 45.108501369475306], [-87.67281427803945, 45.14067236950527], [-87.7296692780924, 45.17660436953874], [-87.7362002780985, 45.19907236955966], [-87.72162827808492, 45.211672369571396], [-87.71966827808309, 45.23677136959477], [-87.70514227806956, 45.247086369604375], [-87.70447127806894, 45.27220536962777], [-87.64536227801389, 45.34816936969852], [-87.64368427801233, 45.36185636971126], [-87.68959827805509, 45.39126936973865], [-87.76003827812069, 45.352897369702916], [-87.82800827818399, 45.35832136970797], [-87.84128227819636, 45.34614936969663], [-87.86209627821574, 45.370165369719004], [-87.86853527822174, 45.37207236972078], [-87.8739742782268, 45.36208536971148], [-87.88361027823578, 45.36585436971499], [-87.84953127820404, 45.40611736975249], [-87.86026727821404, 45.44509836978879], [-87.81361427817059, 45.466460369808686], [-87.78938527814802, 45.499067369839054], [-87.8051412781627, 45.544525369881384], [-87.82860227818455, 45.5685913699038], [-87.78631227814516, 45.56851936990373], [-87.7750752781347, 45.600387369933415], [-87.7760452781356, 45.613200369945346], [-87.81993827817648, 45.65445036998376], [-87.81705427817379, 45.66539036999395], [-87.78094527814017, 45.67591537000375], [-87.77747327813692, 45.684101370011376], [-87.80115627815898, 45.70132437002742], [-87.80155327815935, 45.71139137003679], [-87.84236227819736, 45.722418370047066], [-87.87362927822647, 45.750699370073406], [-87.96917927831547, 45.76644837008807], [-87.99007027833493, 45.795046370114704], [-88.05163927839226, 45.78611237010638], [-88.08873427842681, 45.791532370111426], [-88.12994927846519, 45.81940237013738], [-88.12178627845759, 45.8348783701518], [-88.0654212784051, 45.8736423701879], [-88.09576427843336, 45.89180337020481], [-88.09385027843157, 45.920615370231644], [-88.11139027844791, 45.926287370236935], [-88.15043827848427, 45.93629337024625], [-88.18019427851199, 45.95351637026229], [-88.2149922785444, 45.94790137025706], [-88.25716827858368, 45.9670553702749], [-88.29915227862278, 45.96194437027014], [-88.32132327864343, 45.96671237027458], [-88.3699382786887, 45.994587370300536], [-88.40352227871998, 45.98342237029014], [-88.45431927876729, 46.00076037030629], [-88.48381427879475, 45.99915137030479], [-88.49408327880433, 46.01296037031766], [-88.51561327882438, 46.01860937032291], [-88.54835827885486, 46.019300370323556], [-88.57535727888002, 46.008959370313924], [-88.59753627890068, 46.01551637032003], [-88.6155022789174, 45.99412037030011], [-88.64366927894363, 45.99338837029943], [-88.67738427897504, 46.020144370324346], [-88.70360527899946, 46.01892337032321], [-88.72640927902069, 46.02958137033313], [-88.7730172790641, 46.02114737032528], [-88.77748027906826, 46.032614370335956], [-88.79381527908347, 46.036360370339445], [-88.80439727909332, 46.026804370330545], [-88.92519527920582, 46.07360137037413], [-88.9853012792618, 46.10039137039908], [-89.09980627936845, 46.14564237044122], [-89.9251362801371, 46.30402537058873], [-90.1116592803108, 46.34042937062263], [-90.11517728031409, 46.36515537064566], [-90.14179728033888, 46.39389937067243], [-90.16139128035712, 46.44238037071758], [-90.21152628040382, 46.50629537077711], [-90.25840128044747, 46.508789370779425], [-90.26978528045808, 46.52248037079218], [-90.30018128048638, 46.52505137079457], [-90.30239328048845, 46.544296370812496], [-90.31370828049899, 46.55156337081927], [-90.38552528056586, 46.53965737080817], [-90.40820028058698, 46.568610370835145], [-90.01886428022439, 46.678633370937604], [-89.88625228010088, 46.76893537102171], [-89.79124428001239, 46.824713371073656], [-89.38671827963566, 46.850208371097395], [-89.21459227947535, 46.92337837116554], [-89.12518727939208, 46.99660637123374], [-88.99487527927072, 46.9971033712342], [-88.92968827921001, 47.03092637126571], [-88.88483227916824, 47.104554371334274], [-88.62950027893044, 47.225812371447205], [-88.61810427891983, 47.13111437135902], [-88.51121527882027, 47.106506371336096], [-88.51299527882193, 47.03258937126726], [-88.44116427875504, 46.99073437122827], [-88.4459642787595, 46.92830437117013], [-88.47652327878797, 46.855151371102004], [-88.44661727876012, 46.79939637105008], [-88.17782727850978, 46.94589037118651], [-88.18918827852036, 46.90095837114467], [-88.03668527837834, 46.91186537115482], [-87.90065427825165, 46.90976137115287], [-87.66376627803103, 46.83685137108496], [-87.37153927775887, 46.50799137077868], [-87.11067927751593, 46.501473370772615], [-87.00640227741881, 46.53629337080504], [-86.87138227729307, 46.444359370719425], [-86.75949527718886, 46.48663137075879], [-86.63822027707592, 46.42226337069884], [-86.46239227691217, 46.56108537082814], [-86.14810927661946, 46.67305337093241], [-86.09673927657163, 46.65526837091585], [-85.85753627634885, 46.69481537095268], [-85.50385027601945, 46.67417437093346], [-85.2300942757645, 46.756785371010395], [-84.95475927550807, 46.770951371023585], [-85.02697127557532, 46.694339370952235], [-85.01897527556788, 46.5490243708169], [-85.0516552755983, 46.50557637077644], [-85.0166392755657, 46.476444370749306], [-84.93132027548624, 46.48784337075992], [-84.80365327536734, 46.444054370719144], [-84.62981527520544, 46.48294337075536], [-84.57266727515221, 46.40792637068549], [-84.41596727500628, 46.48065837075323], [-84.31161427490909, 46.48866937076069], [-84.18164627478805, 46.24872037053722], [-84.27313427487326, 46.20730937049865], [-84.24703127484895, 46.17144737046526], [-84.11973527473039, 46.17610837046959], [-84.02957827464643, 46.128943370425674], [-84.06198127467661, 46.094470370393566], [-83.9895012746091, 46.02598537032978], [-83.90195227452757, 46.00590237031108], [-83.90646027453177, 45.96023937026855], [-84.11327227472438, 45.97853837028559], [-84.35448527494903, 45.99919037030483], [-84.50163527508606, 45.97834237028541], [-84.61684527519336, 46.03823037034118], [-84.68902227526058, 46.03591837033903], [-84.73173227530036, 45.855679370171174], [-84.85110027541153, 45.89063637020373], [-85.0616292756076, 46.02475137032863], [-85.37824327590246, 46.100047370398755], [-85.50954627602475, 46.101911370400494], [-85.65538127616057, 45.97287037028032], [-85.859844276351, 45.969469370277146]]
                    state_all[sr.record[0] + 'a'] = {}
                    state_all[sr.record[0] + 'a']['polygon'] = map(lambda x: list(x[::-1]), sr.shape.points)
                    state_all[sr.record[0] + 'a']['demog'] = state_all[sr.record[0]]['demog']
                else:
                    sr.shape.points= sr.shape.points[:killPoint+1]
                    state_all[sr.record[0]]['polygon'] = map(lambda x: list(x[::-1]), sr.shape.points)
                    state_all[sr.record[0]]['demog'] = state_value
            else:
                print sr.record[0]

                #print sr.shape.points
                #print len(sr.shape.points)

                


           # state_all = dict([(sr.record[2], {
            #    'polygon': map(lambda x: list(x[::-1]), sr.shape.points), 
           #     'demog': random.random(),
            #}) for sr in shape.shapeRecords() if sr.record[1] in [25]])
            context['state'] = state_all
                #print sr.shape.points
            

        context['cities'] = cities
        
        if field:
            context['field'] = field
            print field
        return render(request, 'aggregate.html', context)

    def rank_state(self, state_data, field):
        rank_dict = {}
        for x,y in state_data.items():
            rank_dict[x] = y['value'] 
        if field == 'state_data':
            state_sorted = sorted(rank_dict.items(), key=operator.itemgetter(1), reverse=True)
        elif field == 'state_gt':
            state_sorted = sorted(rank_dict.items(), key=operator.itemgetter(1))
        t = {}
        for idx, (x, y )in enumerate(state_sorted):
            t[y] = idx + 1


        for x in state_data:
            state_data[x]['value'] = t[state_data[x]['value']] 
        return state_data

