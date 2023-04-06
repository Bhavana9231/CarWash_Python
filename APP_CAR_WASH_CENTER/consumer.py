'''import json
import asyncio
import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from APP_CAR_WASH_CENTER.models import Booths, Simulation
from channels.db import database_sync_to_async
from django.core.serializers.json import DjangoJSONEncoder





class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(message)
        if message == "Start Simulation":
            

        # Do something with the incoming message
        response = {
            'status': 'success',
            'message': message
        }

        await self.send(text_data=json.dumps(response))'''

import json
import asyncio
import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from APP_CAR_WASH_CENTER.models import Booths, Simulation,Timings
from channels.db import database_sync_to_async
from django.core.serializers.json import DjangoJSONEncoder
from datetime import date,timedelta
from django.db import transaction
from asgiref.sync import sync_to_async

class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        today = date.today()
        print("Today's date:", today)
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def send_json(self, data, cls=None):
        message = json.dumps(data, cls=cls)
        await self.send(message)


    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data['message']
            print(message)
        except json.decoder.JSONDecodeError:
            # Send an error message to the client
            error_message = {'status': 'Invalid message format'}
            await self.send(json.dumps(error_message))
            return
        @database_sync_to_async
        def get_booths():
            today = date.today()
            if Booths.objects.all().filter(Date_1=today).exists():


                booths = Booths.objects.order_by('id').all().filter(Date_1=today)
                print(booths)
                for i in booths:
                    booth_data = Simulation.objects.all().filter(Bid_id = i.id)
                    print(booth_data)
                    
                    for j in booth_data:
                        print(j.Bid_id)
                        duration = Booths.objects.all().filter(id = j.Bid_id).values('Duration')
                        print(duration[0]['Duration'])
                        total_time = int(j.Cars_remaining) * (duration[0]['Duration'])
                        print('id',j.Bid_id)
                        print('total_time',total_time)
                        cars_remaining = j.Cars_remaining
                        print('cars_remaining',cars_remaining)
                        #total_time = j.Total_time_min
                        #print(total_time)
                        current_time = datetime.datetime.now()
                        print(current_time)
                        new_time = current_time + datetime.timedelta(seconds=total_time)
                        print('id',j.Bid_id)
                        print('new_time',new_time)
                        Booths.objects.all().filter(id = j.Bid_id).update(countdown = new_time)

                return list(booths.values('id', 'Type_of_booth', 'Price_NA', 'Price_PA', 'Duration', 'Status', 'countdown'))
            else:
                return None

        @database_sync_to_async
        def get_simulations():
            simulations = Simulation.objects.all()
            return list(simulations.values('id', 'Bid', 'Cars_done', 'Cars_remaining', 'Amount_collected', 'Total_time_taken', 'Date', 'Total_time_min'))


        @database_sync_to_async
        async def get_data(booth_id):
            today = date.today()
            data =Simulation.objects.filter(Bid=booth_id)
            booth_type = data[0].Bid.Type_of_booth
            print(booth_type)
            print('1',data)
            return booth_type
        @database_sync_to_async
        def shift_cars_to_other_booth(current_booth_id, num_cars, simulate):
            print('current_booth_id',current_booth_id)
            current_booth_simulation = Simulation.objects.get(Bid_id=current_booth_id)
            current_booth = Booths.objects.get(id=current_booth_id)
            current_booth_cars_remaining = current_booth_simulation.Cars_remaining
            current_booth_type = current_booth_simulation.Bid.Type_of_booth
            cars = Simulation.objects.all().filter(Bid__Type_of_booth=current_booth_type)
            for i in cars:
                cars_id = i.id
                current_booth_cars_remaining = current_booth_simulation.Cars_remaining
                print('simulate',simulate)
                print('current_booth_type',current_booth_type)
                print('current_booth_id',current_booth_id)
                available_booths = Booths.objects.filter(simulation__id=simulate, Type_of_booth=current_booth_type).exclude(id=current_booth_id).order_by('simulation__Cars_remaining')
                print(available_booths)
                if available_booths.exists():
                    new_booth = available_booths.first()
                    with transaction.atomic():
                        new_booth.simulation.Cars_remaining -= num_cars
                        print(new_booth.simulation.Cars_remaining)
                        new_booth.simulation.save()
                        current_booth.Cars_remaining += num_cars
                        print(current_booth.Cars_remaining)
                        current_booth.save()
                        Simulation.objects.filter(Bid=current_booth_id).update(Bid=new_booth.booth.id)
                        return True
                else:
                    return False
            
        @sync_to_async
        def get_current_booth(booth_id):
            print('1',booth_id)
            return Simulation.objects.get(Bid=booth_id)




        @database_sync_to_async
        def get_timings():
            today = date.today()
            timings = Timings.objects.all().filter(Date_0 = today)
            return list(timings.values('id', 'Stime', 'ETime', 'P1Stime', 'P1Etime', 'P2Stime', 'P2Etime', 'Date_0'))

       

        if message == 'start_timer':
            booth_data = await get_booths()
            simulation_data = await get_simulations()
            timings = await get_timings()
            if booth_data is None:
                await self.send(json.dumps({'status': 'No booths available for the current date'}, cls=DjangoJSONEncoder))
            else:
                data = {'booths': booth_data, 'countdowns': [], 'simulations': simulation_data,'timings':timings}
                # Create a countdown timer for each booth
                for booth in booth_data:
                    print(booth)
                    countdown1 = booth['countdown']
                    #countdown = datetime.datetime.now() + datetime.timedelta(minutes=booth['Duration'])
                    data['countdowns'].append({'id': booth['id'], 'countdown': countdown1})

                # Send the initial data to the client
                await self.send_json(data, cls=DjangoJSONEncoder)



        
        else:


            today = date.today()
            cars_done = data['data']['cars_done']
            print(cars_done)
            cars_remaining = data['data']['cars_remaining']
            print(cars_remaining)
            #simulate = data['data']['simulation_id']
            #print(simulate)
            booth_id = data['data']['id']
            print('booth_id',booth_id)
            price = data['data']['price']
            print(price)
            #time = data['data']['time']
            #print(time)
            timings = await get_timings()
            print(timings)
            Stime = timings[0]['Stime']
            ETime = timings[0]['ETime']

            # Print the extracted values
            print("Stime:", Stime)
            print("ETime:", ETime)
            

    
            #time_in_milliseconds = 1616500000000  # Example time in milliseconds
            '''hours = time / (1000 * 60 * 60)  # Convert milliseconds to hours
                                                print(hours)
                                                current_time = datetime.datetime.now()  # Get the current time
                                    
                                                # Add the calculated hours to the current time
                                                new_time = current_time + datetime.timedelta(hours=hours)
                                    
                                                print(new_time.time())
                                                if Stime <= new_time.time() <= ETime:
                                                    print("Current time is between start and end times")
                                                else:
                                                    print("Current time is not between start and end times")
                                                num_cars = 5
                                                current_booth = await get_current_booth(booth_id)
                                                print('current_booth.id',current_booth.Bid_id)
                                                num_cars = 5  '''
            '''success = await shift_cars_to_other_booth(current_booth.Bid_id, num_cars, simulate)
                                                if success:
                                                    success_message = {'status': 'Cars shifted to another booth successfully'}
                                                    await self.send(json.dumps(success_message))
                                                else:
                                                    error_message = {'status': 'No available booth of the same type with free slots'}
                                                    await self.send(json.dumps(error_message))
                                    '''










            await database_sync_to_async(transaction.on_commit)(
                lambda: Simulation.objects.filter(Bid=booth_id, Date=today).update(Cars_done=cars_done, Cars_remaining=cars_remaining, Amount_collected=price))
            booth_data = await get_booths()
            simulation_data = await get_simulations()
            timings = await get_timings()
            if booth_data is None:
                await self.send(json.dumps({'status': 'No booths available for the current date'}, cls=DjangoJSONEncoder))
            else:
                data = {'booths': booth_data, 'countdowns': [], 'simulations': simulation_data,'timings':timings}
                # Create a countdown timer for each booth
                for booth in booth_data:
                    countdown1 = booth['countdown']
                    #countdown = datetime.datetime.now() + datetime.timedelta(minutes=booth['Duration'])
                    data['countdowns'].append({'id': booth['id'], 'countdown': countdown1})
                #await self.send_json(data, cls=DjangoJSONEncoder)

        #await self.send(json.dumps(data, cls=DjangoJSONEncoder))




        

        

    

