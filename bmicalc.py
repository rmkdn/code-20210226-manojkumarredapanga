from flask_restplus import reqparse, Api, Resource, fields

import json
from flask import Flask, request, Response

import ast

app = Flask(__name__)
api = Api(app)

model_400 = api.model('ErrorResponse400', {'message': fields.String,
		                           'errors' :fields.Raw })

model_500 = api.model('ErrorResponse400', {'status': fields.Integer,
                                           'message':fields.String })

bmi_parser = reqparse.RequestParser()
bmi_parser.add_argument('bmidata', help = 'bmidata', type = str, location='args' , required=True)

@api.route('/bmi_calculation' )
@api.expect (bmi_parser)
class body_mass_index(Resource):
    @api.response(200, 'Successful')
    @api.response(400, 'Validation Error', model_400)
    @api.response(500, 'Internal Processing Error', model_500)

    def get(self):

        args = bmi_parser.parse_args()
        bmi_list = request.args['bmidata']
        #print(type(bmi_list))
        return_status = None
        result = {}
        bmi_final_list = []

        try:

            res = ast.literal_eval(bmi_list)
            for x in res:
                #print(x)
                bmi = x["WeightKg"]/(x["HeightCm"]*x["HeightCm"])*10000
                x['bmi']=bmi
                
                if bmi<=18.4:
                    x['BMI Category']="Under weight"
                    x['Health risk'] = "Malnutrition risk"

                if bmi>=18.5 and bmi<24.9:
                    x['BMI Category']="Normal weight"
                    x['Health risk'] = "Low risk"
                
                if bmi>=25 and bmi<29.9:
                    x['BMI Category']="Over weight"
                    x['Health risk'] = "Enhanced risk"

                if bmi>=30 and bmi<34.9:
                    x['BMI Category']="Moderately Obese"
                    x['Health risk'] = "Medium risk"

                if bmi>=35 and bmi<39.9:
                    x['BMI Category']="Severely obese"
                    x['Health risk'] = "High risk"

                if bmi>40:
                    x['BMI Category']="Very Severely obese"
                    x['Health risk'] = "Very High risk"

                bmi_final_list.append(x)
 
            #print(res,type(res))
            print(bmi_final_list,type(bmi_final_list))
            result['status'] = 1
            result['message'] = "BMI is Calculated"
            return_status = 200
            result['bmi_data'] = bmi_final_list

        except ValueError as e:
            result = {}
            result['status'] = 0
            return_status = 400
            result['message'] = e.args[0]
        except Exception as e:
            result = {}
            return_status = 500
            result['status'] = 0
            result['message'] = 'Internal Error has occurred while processing the request'
        finally:
            resp = Response(json.dumps(result), status=return_status, mimetype="application/json")
        return resp

if __name__ =='__main__':
  port =  8001  
  app.run(host='0.0.0.0', port=port)
