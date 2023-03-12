from django.shortcuts import render
import joblib
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


def flights(request):
    data = {
        "title" : "SKYY | Flights",
        "color" : "white",
        "css" : "/static/css/style_flight.css",
    }

    try:
        if request.method == "POST":
            ans = ''
            N_Stops = 0
            L1 = "None"
            L2 = "None"
            Src = request.POST["Src"]
            Dest = request.POST["Dest"]
            D_Date_Time = request.POST["D_Date_Time"]
            A_Date_Time = request.POST["A_Date_Time"]
            Airl = request.POST["Airl"]
            Seats = request.POST["seats"]
            
            try:
                L1 = request.POST["L1"]
                N_Stops = 1
                try:
                    L2 = request.POST["L2"]
                    N_Stops = 2
                except:
                    pass
            except:
                pass

            loaded_leSource = joblib.load('label_encoder_source.pkl')
            loaded_leDest = joblib.load('label_encoder_destination.pkl')
            loaded_leAirline = joblib.load('label_encoder_airline.pkl')

            Src_New = loaded_leSource.transform([Src])
            Dest_New = loaded_leDest.transform([Dest])
            Airl_New = loaded_leAirline.transform([Airl])

            D_Date_Time_New = datetime.strptime(D_Date_Time, '%Y-%m-%dT%H:%M')
            A_Date_Time_New = datetime.strptime(A_Date_Time, '%Y-%m-%dT%H:%M')

            D_Date_Time_New1 = D_Date_Time_New.strftime("%d-%b-%Y %H:%M")
            A_Date_Time_New1 = A_Date_Time_New.strftime("%d-%b-%Y %H:%M")

            Day = D_Date_Time_New.day
            Month = D_Date_Time_New.month
            TTH = round((A_Date_Time_New - D_Date_Time_New).total_seconds() / 60 / 60, 2)

            if N_Stops == 0:
                loaded_model = joblib.load("farePrediction_model_RFR_oneWay.pkl")

                prediction = loaded_model.predict([[Src_New[0], Dest_New[0], Airl_New[0], N_Stops, Day, Month, TTH]])
                ans = int(prediction[0])
                print("OneWay: ", ans)

                data = {
                    "title" : "SKYY | Ticket",
                    "color" : "#0047AB;",
                    "css" : "/static/css/style_ticket.css",
                    "n" : N_Stops,
                    "Src" : Src,
                    "Des" : Dest,
                    "DDT" : D_Date_Time_New1,
                    "ADT" : A_Date_Time_New1,
                    "Airl" : Airl,
                    "Seats" : Seats,
                    "TTH" : TTH,
                    "Ans" : ans
                }
            elif N_Stops == 1:
                loaded_leLayover1 = joblib.load('label_encoder_layover1.pkl')
                L1_New = loaded_leLayover1.transform([L1])

                loaded_model = joblib.load("farePrediction_model_RFR_multiCity1.pkl")

                prediction = loaded_model.predict([[Src_New[0], L1_New[0], Dest_New[0], Airl_New[0], N_Stops, Day, Month, TTH]])
                ans = int(prediction[0])
                print("Multicity-1: ", ans)

                data = {
                    "title" : "SKYY | Ticket",
                    "color" : "#0047AB;",
                    "css" : "/static/css/style_ticket.css",
                    "n" : N_Stops,
                    "Src" : Src,
                    "L1" : L1,
                    "Des" : Dest,
                    "DDT" : D_Date_Time_New1,
                    "ADT" : A_Date_Time_New1,
                    "Airl" : Airl,
                    "Seats" : Seats,
                    "TTH" : TTH,
                    "Ans" : ans
                }
            else:
                loaded_leLayover1 = joblib.load('label_encoder_layover1.pkl')
                L1_New = loaded_leLayover1.transform([L1])
                loaded_leLayover2 = joblib.load('label_encoder_layover2.pkl')
                L2_New = loaded_leLayover2.transform([L2])

                loaded_model = joblib.load("farePrediction_model_RFR_multiCity2.pkl")

                prediction = loaded_model.predict([[Src_New[0], L1_New[0], L2_New[0], Dest_New[0], Airl_New[0], N_Stops, Day, Month, TTH]])
                ans = int(prediction[0])
                print("Multicity-2: ", ans)

                data = {
                    "title" : "SKYY | Ticket",
                    "color" : "#0047AB;",
                    "css" : "/static/css/style_ticket.css",
                    "n" : N_Stops,
                    "Src" : Src,
                    "L1" : L1,
                    "L2" : L2,
                    "Des" : Dest,
                    "DDT" : D_Date_Time_New1,
                    "ADT" : A_Date_Time_New1,
                    "Airl" : Airl,
                    "Seats" : Seats,
                    "TTH" : TTH,
                    "Ans" : ans
                }

            return render(request, "tickets.html", data)
    except:
        print("Exception")
        pass

    return render(request, "flights.html", data)
