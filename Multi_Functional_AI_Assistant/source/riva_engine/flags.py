f1 = "open notepad"
f2 = "open command prompt"
f3 = "open cmd"
f4 = "open camera"
f5 = "open calculator"
f6 = "ip address"
f7 = "wikipedia"
f8 = "youtube"
f9 = "search on google"
f10 = "send whatsapp message"
f11 = "send an email"
f12 = "joke"
f13 = "advice"
f14 = "trending movies"
f15 = "news" 
f16 = "weather"
f17 = "convert currency"
f18 = "face recognition"
f19 = "object detection"
f20 = 'what do you see'
f21 = "terminate process"

arrayOfFlags = [f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12, f13, f14, f15, f16, f17, f18, f19, f20, f21]  

def search_flag(query):
    count = 0
    query = query.lower()
    print(query)
    for f in arrayOfFlags:
        if f in query:
            return True
        elif count == len(arrayOfFlags) -1:
            return False
        else:
            count += 1
    
