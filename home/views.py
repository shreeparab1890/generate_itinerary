from django.shortcuts import render, HttpResponse
from django.contrib import messages
import io
import openai

import spacy
nlp = spacy.load("en_core_web_sm")


def GTP_APP(text):
    openai.api_key="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"
    res=openai.Completion.create(
    model='text-davinci-003',
    prompt=text,
    max_tokens=2500,
    temperature=0.6,
    frequency_penalty=1,
    presence_penalty= 1)
    return res.choices[0].text

def makeItinerary(days,destination,interest):
    itinerary = GTP_APP("give an in detail travel itinerary with perfect Punctuation importantly ending each sentence with full stop w.r.t. each day starting with Breakfast, what to do in the first half naming it as 'Morning Activity', what to have for Lunch naming it as 'Lunch', what to do in the second half naming it as 'Evening activity' and how to spend the night naming it as 'Night' for "+days+" days in "+destination+"  w.r.t. user interests like " +interest+". and compulsarily end every day with &&")
    #places = GTP_APP(itinerary+" identify the named entity recognition separated by | from the given text related to "+destination+" places and "+destination+" clubs")
    #places_list = places.split("|")
    #goan_places = []
    #for place in places_list:
    #    goan_places.append(place.strip())

    doc = nlp(itinerary)
    places_list = []
    for ent in doc.ents:
        if ent.label_ == "GPE" or ent.label_ == "ORG" or ent.label_ == "LOC":
            places_list.append(ent.text)
    
    i = 0
    for place in places_list:
        if i == 0:
            new_itinerary = itinerary.replace(place, "<NER>"+place+"</NER>")
        
            i = i + 1
        else:
            new_itinerary = new_itinerary.replace(place, "<NER>"+place+"</NER>")


    ##itinerary =  "\n\nDay 1: \nMorning breakfast: Start the day with local Goan specialties like Khatkhate, Prawn Balchao and Poee at a traditional restaurant in Panjim. \nDistance from hotel: 10 km  \nMorning Activity: Head to Colva beach for some sunbathing, swimming or just lazing around. Enjoy water sports activities like windsurfing, jet skiing and parasailing here. Distance from hotel: 35km  \nLunch: Have lunch at one of the shacks on Colva beach serving delicious seafood dishes such as tisryo sukhem (prawn curry) and mackerel recheado (spicy grilled fish).  Distance from hotel : 35km \n Evening activity : Explore the offbeat side of Goa by taking a boat ride down River Sal to spot wild dolphins in their natural habitat . Distance from Hotel : 50 km  \n Night : End your day with some shopping at Anjuna Flea Market where you can buy souvenirs , handmade jewellery and clothes .Distance from Hotel : 65 km &&\n\n Day 2:  Morning breakfast : Try out authentic Portuguese treats like pastel de nata (custard tart) , bolinhos de bacalhau (codfish cakes )at Cafe Chocolatti in Dona Paula .Distance from Hotel : 25 km   \n Morning Activity: Visit old churches such as Se Cathedral church , Basilica of Bom Jesus Church & St Francis Xavier’s Church which are known for their beautiful architecture .Distance From Hotel - 30Km   Lunch - Sample sumptuous seafood thalis served with rice and roti at La Plage Restaurant located near Miramar Beach . Distance From Hotel- 25Km     Evening activity- Take a sunset cruise along Mandovi River to soak up serene views of backwaters & mangroves accompanied by live music performance onboard. Distance From Hotel - 15Km    Night – Catch an exotic fire show performed by professional dancers outside Tito’s Club near Baga Beach. You can also enjoy drinks while watching the show! Distance From Hotel - 55Km &&\n\n Day 3 – Morning Breakfast – Feast on scrumptious pancakes topped with fruits & honey alongwith coffee/ tea at Artjuna Café in Vagator Beach. The café has an outdoor seating area overlooking lush greenery all around ! Distance From Hotel – 45Km     \tMorning Activity– Spend time birdwatching or trekking through dense forests inside Bhagwan Mahavir Wildlife Sanctuary located close to Molema Village . Spot various species including Kingfishers, Malabar Grey Hornbills etc here !Distance From Hotels - 75 Kms        Lunch– Relish lip smacking vegetarian delicacies such as vegetable xacuti & vindaloo prepared using fresh ingredients sourced locally at Namaste Café located inside Ashwem beach premises. distanceFromHotel-60km    Evening activity– Soak up stunning views of Dudhsagar Waterfalls while trekking through its nearby forests followed by relaxing dip into cool waters ! distancefromhotel-90km       Night– Dance away your evening amidst pulsating beats played by international DJs playing EDM tracks inside Hilltop Club situated atop Anjuna Hill!distancefromhotel-70km&&\n\n Day 4 – Morning Breakfast – Begin your last day exploring goa with tasty sandwiches filled with veggies/ cheese served alongside hot chai /coffee available across street food stalls in Panaji city centre!distancefromhotel-10 kms. Morning Activity– Take part in optional yoga classes held every morning on Morjim beach surrounded by peaceful ambience created due to pristine white sands stretching far away into sea waters!distanceFromHotel-85 Kms. Lunch– Indulge yourself into some authentic Konkan cuisine comprising spicy pomfret fry/ crab masala accompanied steamed rice/ chapattis served under swaying coconut trees near Arambol beach shoreline !distanceFromHotel-95 kms. Evening Activity– Enjoy thrilling rides offered inside Snow Park located within MES College Campus offering snow slides & other ice based attractions during summer season making it perfect outing option for family fun! distance from hotel to park 50kms.     Night– Conclude this trip relishing mouth watering seafood platters consisting crabs/ lobsters cooked according to individual taste buds preference served beside bonfire setup besides Calangute beaschside providing mesmerising view of setting sun over Arabian Sea waters!. &&" 
    day_itinerary = new_itinerary.split("&&")
    
    detail_iti = {}
    for day in range(int(days)):
        detail_iti[day] = day_itinerary[day].split(".")
    list_dtl_iti = []
    for day in range(int(days)):   
        list_dtl_iti.append({"name":detail_iti[day]})
    
    return list_dtl_iti,places_list

def testFun():
    list1 = [{'name':'Shree', 'age':20},{'name':'abc', 'age':21},{'name':'xyz', 'age':22},{'name':'lmn', 'age':23}]
    return list1

def index(request):
    if request.method == "POST":
        destination = request.POST.get('destination')
        days = request.POST.get('days')
        interest = request.POST.get('interest')
        itinerary,places_list = makeItinerary(days,destination,interest)
        
        
        context = {
            "days_itinerary":list(itinerary),
            "places_list": places_list
        }
        messages.success(request, "Itinerary Generated Succesfully")
        return render(request, 'index.html', context)
    return render(request, 'index.html')

def about(request):
    
    return render(request, 'about.html')
    