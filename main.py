from flask import Flask, render_template, url_for, redirect
#from app import app
from form import AddressForm, SearchForm
import json
from flask import request
from urllib.parse import urlencode, urljoin, urlparse, parse_qs

app = Flask(__name__)

app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'

@app.route('/', methods=['GET','POST'])
def Add():
    status=""
    form = AddressForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        phone = form.phone.data
        email = form.email.data
        x = {
            "first_name": first_name,
            "last_name": last_name,
            "phone": phone,
            "email": email
            }
        with open('data.json', 'r+') as f:
            file_data= json.load(f)
            file_data['addresses'].append(x)
            f.seek(0)
            json.dump(file_data, f, indent = 4)
            status = "Address added"
        
    return render_template('add.html',form=form, status=status)
    #with open('data.json','r') as f:
     #   table = json.loads(f.read())
      #  print(table)
       # return table
    #for address in state_data['addresses']:
     #   print(address)

@app.route('/All', methods=['GET','POST'])
def listAll():
    with open('data.json','r') as f:
        table = json.loads(f.read())
        return render_template('table.html', table=table)
    

@app.route('/search',methods=['GET','POST'])
def Search():
    status=""
    content=""
    form = SearchForm()
    if form.validate_on_submit():
        first_name= form.first_name.data
        #status = found
        with open('data.json','r') as f:
            file_data= json.load(f)
            # content = file_data
            addresses = file_data['addresses']
            for address in addresses:
                if address['first_name'] == first_name:
                    content = address
                    status = "found"
        
        if status != "found":
            status = "not found"

    return render_template('list.html',form=form, status=status, content=content)


@app.route('/edit',methods=['GET','POST'])
def edit():
    status=""
    content=""
    new_url=""
    form = SearchForm()
    if form.validate_on_submit():
        first_name= form.first_name.data
        #status = found
        with open('data.json','r') as f:
            file_data= json.load(f)
            # content = file_data
            addresses = file_data['addresses']
            for address in addresses:
                if address['first_name'] == first_name:
                    content = [address['first_name'], address['last_name']]
                    new_url = urlencode(address)
                    status = "found_for_edit"
    return render_template('edit.html',form=form, status=status, content=content, new_url = new_url)


@app.route('/editing',methods=['GET','POST'] )
def edit2():
    status=""
    file_data=""
    form = AddressForm()
    captured_value1=request.args.get('first_name')
    captured_value2=request.args.get('last_name')
    captured_value3=request.args.get('phone')
    captured_value4=request.args.get('email')
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        phone = form.phone.data
        email = form.email.data
        x = {
            "first_name": first_name,
            "last_name": last_name,
            "phone": phone,
            "email": email
            }
        with open('data.json', 'r+') as f:
            file_data= json.load(f)
            addresses = file_data['addresses']
            for address in addresses:
                if (address['first_name'] == captured_value1) and (address['last_name'] == captured_value2) and (address['phone'] == captured_value3) and (address['email'] == captured_value4):
                    address['first_name'] = first_name
                    address['last_name'] = last_name
                    address['phone'] = phone
                    address['email']= email
                    
        f.close()
        with open('data.json',"w") as f:
            json.dump(file_data, f, indent = 4)
            status = "edited data saved"
        f.close()
    
    captured_value = {
        "first_name": captured_value1,
        "last_name": captured_value2,
        "phone": captured_value3,
        "email": captured_value4
    }

    return render_template('editing.html',form=form, captured_value=captured_value, status=status)
        
@app.route('/delete',methods=['GET','POST'] )
def delete():
    status=""
    file_data=""
    captured_value1=request.args.get('first_name')
    captured_value2=request.args.get('last_name')
    captured_value3=request.args.get('phone')
    captured_value4=request.args.get('email')
    with open('data.json', 'r+') as f:
        file_data= json.load(f)
        addresses = file_data['addresses']  
        new_data = []
        newfile_data = {"addresses":[]} 
        for address in addresses:
            if (address['first_name'] != captured_value1) and (address['last_name'] != captured_value2) and (address['phone'] != captured_value3) and (address['email'] != captured_value4):
                new_address = {
                    "first_name": address['first_name'],
                    "last_name": address['last_name'],
                    "phone": address['phone'],
                    "email": address['email']
                }
                # new_data.append(new_address) 
                newfile_data['addresses'].append(new_address)
                f.seek(0)
        final_data = newfile_data
    f.close()
    with open('data.json',"w") as f:
        json.dump(final_data, f, indent = 4)
        status = "selected address data deleted"
    f.close()
    return redirect(url_for("Add"))



        


if __name__ == '__main__':
	app.run(debug=True)