from flask import Flask, render_template, request 
from datetime import datetime
import json
from web3 import Web3, HTTPProvider
import os
import datetime

app = Flask(__name__)


global details, scode


def readDetails(contract_type):
    global details
    details = ""
    blockchain_address = 'http://127.0.0.1:8545' #Blokchain connection IP
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'Product.json' #counter feit contract code
    deployed_contract_address = '0xdC355Fa8b439638bC749A360d7C645a2A26841f8' #hash address to access counter feit contract
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi) #now calling contract to access data
    if contract_type == 'adduser':
        details = contract.functions.getUsers().call()
    if contract_type == 'product':
        details = contract.functions.getproduct().call()
    if contract_type == 'order':
        details = contract.functions.getorder().call()
    if contract_type == 'history':
        details = contract.functions.gethistory().call()
    if len(details) > 0:
        if 'empty' in details:
            details = details[5:len(details)]

    
    

      

def saveDataBlockChain(currentData, contract_type):
    global details
    global contract
    details = ""
    blockchain_address = 'http://127.0.0.1:8545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'Product.json' #Counter feit contract file
    deployed_contract_address = '0xdC355Fa8b439638bC749A360d7C645a2A26841f8' #contract address
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    readDetails(contract_type)
    if contract_type == 'adduser':
        details+=currentData
        msg = contract.functions.addUsers(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    if contract_type == 'product':
        details+=currentData
        msg = contract.functions.addproduct(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    if contract_type == 'order':
        details+=currentData
        msg = contract.functions.addorder(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    if contract_type == 'history':
        details+=currentData
        msg = contract.functions.addhistory(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)


@app.route('/AddSellerAction', methods=['POST'])
def AddSellerAction():
    if request.method == 'POST':
        sname = request.form['t1']
        password = request.form['t2']
        sbrand = request.form['t3']
        scode = request.form['t4']
        snumber = request.form['t5']
        smanager = request.form['t6']
        saddress = request.form['t7']

        status = "none"
        readDetails('adduser')
        arr = details.split("\n")

        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == 'Seller' and array[1] == sname and array[4] == scode:
                status ="Username or Seller Code already exists"
                context = status  
                return render_template('AddSeller.html', msg=context)
                break

        if status == "none":
            data = "Seller"+"#"+sname+"#"+password+"#"+sbrand+"#"+scode+"#"+snumber+"#"+smanager+"#"+saddress+"\n"
            saveDataBlockChain(data, "adduser")
            context = "SignUp Completed and details are saved to blockchain"  
            return render_template('AddSeller.html', msg=context)
        else:
            context = 'Error in signup process'  
            return render_template('AddSeller.html', msg=context)

@app.route('/AdminAction', methods=['POST'])
def AdminAction():
    if request.method == 'POST':
        username = request.form['t1']
        password = request.form['t2']


        if username == "Admin" and password == "Admin":
            context = "Welcome Manufacturer"
            return render_template('AdminScreen.html', msg=context)
        else:
            context = "Invalid Login Details"
            return render_template("AdminLogin.html", msg=context)


    
@app.route('/AddProductAction', methods=['POST'])
def AddProductAction():
    if request.method == 'POST':
        pname = request.form['t1']
        psn = request.form['t2']
        scode = request.form['t3']
        pbrand = request.form['t4']
        pcolor = request.form['t5']
        pprice = request.form['t6']
        psize = request.form['t7']

        status = "none"
        readDetails('product')
        arr = details.split("\n")

        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[1] == pname and array[2] == psn:
                status = "Product already exists"
                context = status  
                return render_template('AddProduct.html', msg=context)
                break

        if status == "none":
            data = 'Manufacturer#'+pname+"#"+psn+"#"+scode+"#"+pbrand+"#"+pcolor+"#"+pprice+"#"+psize+"#"+"\n"
            saveDataBlockChain(data, "product")
            context = "Product details are added to blockchain"  
            return render_template('AddProduct.html', msg=context)
        else:
            context = 'Error in the process'  
            return render_template('AddProduct.html', msg=context)

            

@app.route('/SellerLoginAction', methods=['POST'])
def SellerLoginAction():
    if request.method == 'POST':
        global scode
        username = request.form['t1']
        password = request.form['t2']
        
        status = "none"
        readDetails('adduser')
        arr = details.split("\n")

        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == 'Seller' and array[1] == username and array[2] == password:
                scode = array[4]
                status = 'success'
                break

        if status == 'success':
            context = 'Welcome ' + username
            return render_template('SellerScreen.html', msg=context)
        else:
            context = 'Invalid Login Details'
            return render_template('SellerLogin.html', msg=context)


def product_is_purchased(name):
    readDetails('history')
    arr = details.split("\n")

    for i in range(len(arr)-1):
        array = arr[i].split("#")

        if array[0] == 'Seller' and array[1] == name:
            return True
            break

    return False


@app.route('/SellProduct', methods=['GET', 'POST'])
def SellProduct():
    if request.method == 'GET':
        global scode
        output = '<table border="1" align="center" width="100%">'
        font = '<font size="3" color="black">'
        headers = ['Product Name', 'Product Serial Number', 'Seller Code', 'Seller Brand', 'Product Colour', 'Product Price', 'Product Size', 'Action']

        output += '<tr>'
        for header in headers:
            output += f'<th>{font}{header}{font}</th>'
        output += '</tr>'

        readDetails('product')
        arr = details.split("\n")

        for i in range(len(arr)-1):
            array = arr[i].split("#")

            if array[0] == 'Manufacturer' and array[3] == scode:
                output += '<tr>'
                for cell in array[1:8]:
                    output += f'<td>{font}{cell}{font}</td>'
                if product_is_purchased(array[1]):
                    output += f'<td>{font}Already Purchased{font}</td>'
                else:
                    output += f'<td><a href="/Purchase?pname={array[1]}">{font}Click Here{font}</a></td>'
                output += '</tr>'

        output += '</table><br/><br/><br/>'

        return render_template('SellProduct.html', msg=output)



@app.route('/Purchase', methods=['GET'])
def purchase():
    pname = request.args.get('pname')
    
    if pname is None:
        context = 'Product name not provided.'
    else:
        readDetails('product')
        arr = details.split("\n")
        
        for item in arr:
            data = item.split("#")
            if data[1] == pname:
                pname, psn, scode, pbrand, pcolor, pprice, psize = data[1:8]
                data = 'Seller#'+pname+"#"+psn+"#"+scode+"#"+pbrand+"#"+pcolor+"#"+pprice+"#"+psize+"#"+"\n"
                data1 = 'Seller'+"#"+pname+"\n"
                saveDataBlockChain(data, "order")
                saveDataBlockChain(data1,"history")
                context = 'Purchase Made Successfully.'
                break
        else:
            context = 'Product not found.'

    return render_template('Purchase.html', msg=context)


@app.route('/AddCustomerAction', methods=['POST'])
def AddCustomerAction():
    if request.method == 'POST':
        cnmae = request.form['t1']
        password = request.form['t2']
        cemail = request.form['t3']
        cnumber = request.form['t4']
        caddress = request.form['t5']

        status = "none"
        readDetails('adduser')
        arr = details.split("\n")

        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == 'Customer' and array[1] == cnmae:
                status ="Username already exists"
                context = status  
                return render_template('AddCustomer.html', msg=context)
                break

        if status == "none":
            data = "Customer#"+cnmae+"#"+password+"#"+cemail+"#"+cnumber+"#"+caddress+"\n"
            saveDataBlockChain(data, "adduser")
            context = "SignUp Completed and details are saved to blockchain"  
            return render_template('AddCustomer.html', msg=context)
        else:
            context = 'Error in signup process'  
            return render_template('AddCustomer.html', msg=context)

@app.route('/CustomerLoginAction', methods=['POST'])
def CustomerLoginAction():
    if request.method == 'POST':
        username = request.form['t1']
        password = request.form['t2']
        
        status = "none"
        readDetails('adduser')
        arr = details.split("\n")

        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == 'Customer' and array[1] == username and array[2] == password:
                scode = array[4]
                status = 'success'
                break

        if status == 'success':
            context = 'Welcome ' + username
            return render_template('CustomerScreen.html', msg=context)
        else:
            context = 'Invalid Login Details'
            return render_template('CustomerLogin.html', msg=context)


@app.route('/AuthenticationAction', methods=['POST'])
def AuthenticationAction():
    if request.method == 'POST':
        psn = request.form['t1']
        
        status = "none"
        readDetails('product')
        arr = details.split("\n")

        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == 'Manufacturer' and  array[2] == psn:
                status = 'success'
                break

        if status == 'success':
            context = 'Product is genuine.'
            return render_template('Authentication.html', msg=context)
        else:
            context = 'Fake Product.'
            return render_template('Authentication.html', msg=context)


def product_is_purchase(name):
    readDetails('history')
    arr = details.split("\n")

    for i in range(len(arr)-1):
        array = arr[i].split("#")

        if array[0] == 'Customer' and array[1] == name:
            return True
            break

    return False




@app.route('/OrderProduct', methods=['GET', 'POST'])
def OrderProduct():
    if request.method == 'GET':
        output = '<table border="1" align="center" width="100%">'
        font = '<font size="3" color="black">'
        headers = ['Product Name', 'Product Serial Number', 'Seller Code', 'Seller Brand', 'Product Colour', 'Product Price', 'Product Size', 'Action']

        output += '<tr>'
        for header in headers:
            output += f'<th>{font}{header}{font}</th>'
        output += '</tr>'

        readDetails('order')
        arr = details.split("\n")

        unique_product_names = set()
        

        for i in range(len(arr) - 1):
            array = arr[i].split("#")

            if array[0] == 'Seller':
                product_name = array[1]

                if product_name not in unique_product_names:
                    unique_product_names.add(product_name)
                    output += '<tr>'
                    for cell in array[1:8]:
                        output += f'<td>{font}{cell}{font}</td>'

                    if product_is_purchase(array[1]):
                        output += f'<td>{font}Already Purchased{font}</td>'
                    else:
                        output += f'<td><a href="/Buy?pname={array[1]}">{font}Click Here{font}</a></td>'
                    output += '</tr>'

        output += '</table><br/><br/><br>'

        return render_template('OrderProduct.html', msg=output)



@app.route('/Buy', methods=['GET'])
def Buy():
    pname = request.args.get('pname')
    
    if pname is None:
        context = 'Product name not provided.'
    else:
        readDetails('product')
        arr = details.split("\n")
        
        for item in arr:
            data = item.split("#")
            if data[1] == pname:
                pname, psn, scode, pbrand, pcolor, pprice, psize = data[1:8]
                current_time = datetime.datetime.now()
                data = 'Customer#'+pname+"#"+psn+"#"+scode+"#"+pbrand+"#"+pcolor+"#"+pprice+"#"+psize+"#"+str(current_time)+"\n"
                data1 = 'Customer'+"#"+pname+"\n"
                saveDataBlockChain(data, "order")
                saveDataBlockChain(data1, "history")
                context = 'Purchase Made Successfully.'
                break
        else:
            context = 'Product not found.'

    return render_template('Buy.html', msg=context)


@app.route('/ViewSeller',methods=['GET','POST'])
def ViewSeller():
    if request.method == 'GET':
        output = '<table border="1" align="center" width="100%">'
        font = '<font size="3" color="black">'
        headers = ['Seller Name', 'Password', 'Seller Brand', 'Seller Code', 'Seller Number', 'Seller Manager', 'Seller Address']
        unique_seller_names = set()

        output += '<tr>'
        for header in headers:
            output += f'<th>{font}{header}{font}</th>'
        output += '</tr>'

        readDetails('adduser')
        arr = details.split("\n")

        for i in range(len(arr) - 1):
            array = arr[i].split("#")

            if array[0] == 'Seller':
                sellername = array[1]

                
                if sellername not in unique_seller_names:
                    unique_seller_names.add(sellername)

                    output += '<tr>'
                    for cell in array[1:8]:
                        output += f'<td>{font}{cell}{font}</td>'
                   

        output += '</table><br/><br/><br/>'

        return render_template('ViewSeller.html', msg=output)

@app.route('/ViewCustomer',methods=['GET','POST'])
def ViewCustomer():
    if request.method == 'GET':
        output = '<table border="1" align="center" width="100%">'
        font = '<font size="3" color="black">'
        headers = ['Customer Name', 'Password', 'Email', 'Number', 'Address']
        unique_customer_names = set()

        output += '<tr>'
        for header in headers:
            output += f'<th>{font}{header}{font}</th>'
        output += '</tr>'

        readDetails('adduser')
        arr = details.split("\n")

        for i in range(len(arr) - 1):
            array = arr[i].split("#")

            if array[0] == 'Customer':
                customername = array[1]

                
                if customername not in unique_customer_names:
                    unique_customer_names.add(customername)

                    output += '<tr>'
                    for cell in array[1:6]:
                        output += f'<td>{font}{cell}{font}</td>'
                   

        output += '</table><br/><br/><br/>'

        return render_template('ViewCustomer.html', msg=output)


@app.route('/ViewTransaction', methods=['GET', 'POST'])
def ViewTransaction():
    if request.method == 'GET':
        global scode
        output = '<table border="1" align="center" width="100%">'
        font = '<font size="3" color="black">'
        headers = ['Product Name', 'Product Serial Number', 'Seller Code', 'Seller Brand', 'Product Colour', 'Product Price', 'Product Size', 'Purchased Time']

        output += '<tr>'
        for header in headers:
            output += f'<th>{font}{header}{font}</th>'
        output += '</tr>'

        readDetails('order')
        arr = details.split("\n")

        unique_product_names = set()  

        for i in range(len(arr) - 1):
            array = arr[i].split("#")

            if array[0] == 'Customer':
                product_name = array[1]

                
                if product_name not in unique_product_names:
                    output += '<tr>'
                    for cell in array[1:9]:
                        output += f'<td>{font}{cell}{font}</td>'
                    unique_product_names.add(product_name)  

        output += '</table><br/><br/><br/>'

        return render_template('ViewTransaction.html', msg=output)

@app.route('/ViewBuy', methods=['GET', 'POST'])
def ViewBuy():
    if request.method == 'GET':
        global scode
        output = '<table border="1" align="center" width="100%">'
        font = '<font size="3" color="black">'
        headers = ['Product Name', 'Product Serial Number', 'Seller Code', 'Seller Brand', 'Product Colour', 'Product Price', 'Product Size', 'Purchased Time']

        output += '<tr>'
        for header in headers:
            output += f'<th>{font}{header}{font}</th>'
        output += '</tr>'

        readDetails('order')
        arr = details.split("\n")

        unique_product_names = set()  

        for i in range(len(arr) - 1):
            array = arr[i].split("#")

            if array[0] == 'Customer':
                product_name = array[1]

                
                if product_name not in unique_product_names:
                    output += '<tr>'
                    for cell in array[1:9]:
                        output += f'<td>{font}{cell}{font}</td>'
                    unique_product_names.add(product_name)  

        output += '</table><br/><br/><br/>'

        return render_template('ViewBuy.html', msg=output)



@app.route('/ViewTransactionAction', methods=['GET', 'POST'])
def ViewTransactionAction():
    if request.method == 'GET':
        global scode 
        output = '<table border="1" align="center" width="100%">'
        font = '<font size="3" color="black">'
        headers = ['Product Name', 'Product Serial Number', 'Seller Code', 'Seller Brand', 'Product Colour', 'Product Price', 'Product Size', 'Purchased Time']

        output += '<tr>'
        for header in headers:
            output += f'<th>{font}{header}{font}</th>'
        output += '</tr>'

        readDetails('order')
        arr = details.split("\n")

        unique_product_names = set()  

        for i in range(len(arr) - 1):
            array = arr[i].split("#")

            if array[0] == 'Customer' and array[3] == scode:
                product_name = array[1]

                
                if product_name not in unique_product_names:
                    output += '<tr>'
                    for cell in array[1:9]:
                        output += f'<td>{font}{cell}{font}</td>'
                    unique_product_names.add(product_name)  

        output += '</table><br/><br/><br/>'

        return render_template('ViewTransactionAction.html', msg=output)




@app.route('/AddProduct', methods=['GET', 'POST'])
def AddProduct():
    if request.method == 'GET':
       return render_template('AddProduct.html', msg='')


@app.route('/AdminLogin', methods=['GET', 'POST'])
def AdminLogin():
    if request.method == 'GET':
       return render_template('AdminLogin.html', msg='')

@app.route('/ViewBuy', methods=['GET', 'POST'])
def ViewBuys():
    if request.method == 'GET':
       return render_template('ViewBuy.html', msg='')

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
       return render_template('index.html', msg='')

@app.route('/ViewTransactionAction', methods=['GET', 'POST'])
def ViewTransactionActions():
    if request.method == 'GET':
       return render_template('ViewTransactionAction.html', msg='')

@app.route('/ViewTransaction', methods=['GET', 'POST'])
def ViewTransactions():
    if request.method == 'GET':
       return render_template('ViewTransaction.html', msg='')

@app.route('/ViewCustomer', methods=['GET', 'POST'])
def ViewCustomers():
    if request.method == 'GET':
       return render_template('ViewCustomer.html', msg='')

@app.route('/Authentication', methods=['GET', 'POST'])
def Authentication():
    if request.method == 'GET':
       return render_template('Authentication.html', msg='')

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
       return render_template('index.html', msg='')

@app.route('/AdminScreen', methods=['GET', 'POST'])
def AdminScreen():
    if request.method == 'GET':
       return render_template('AdminScreen.html', msg='')
    
@app.route('/SellerScreen', methods=['GET', 'POST'])
def SellerScreen():
    if request.method == 'GET':
       return render_template('SellerScreen.html', msg='')

@app.route('/SellerLogin', methods=['GET', 'POST'])
def SellerLogin():
    if request.method == 'GET':
       return render_template('SellerLogin.html', msg='')

@app.route('/SellProduct', methods=['GET', 'POST'])
def SellProducts():
    if request.method == 'GET':
       return render_template('SellProduct.html', msg='')

@app.route('/AddSeller', methods=['GET', 'POST'])
def AddSeller():
    if request.method == 'GET':
       return render_template('AddSeller.html', msg='')


@app.route('/AddCustomer', methods=['GET', 'POST'])
def AddCustomers():
    if request.method == 'GET':
       return render_template('AddCustomer.html', msg='')


@app.route('/CustomerScreen', methods=['GET', 'POST'])
def CustomerScreen():
    if request.method == 'GET':
       return render_template('CustomerScreen.html', msg='')


@app.route('/CustomerLogin', methods=['GET', 'POST'])
def CustomerLogins():
    if request.method == 'GET':
       return render_template('CustomerLogin.html', msg='')



@app.route('/OrderProduct', methods=['GET', 'POST'])
def OrderProducts():
    if request.method == 'GET':
       return render_template('OrderProduct.html', msg='')

@app.route('/Buy', methods=['GET', 'POST'])
def Buys():
    if request.method == 'GET':
       return render_template('Buy.html', msg='')

@app.route('/ViewSeller', methods=['GET', 'POST'])
def ViewSellers():
    if request.method == 'GET':
       return render_template('ViewSeller.html', msg='')


            
        
if __name__ == '__main__':
    app.run()       
