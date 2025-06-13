from flask import Flask, request
import threading

app = Flask(__name__)
STOCK_FILE = 'stock.txt'
lock = threading.Lock()  # Lock untuk menghindari race condition

@app.route('/buy', methods=['POST'])
def buy():
    item = request.form.get('item', 'banana')
    qty = int(request.form.get('qty', '1'))

    with lock:  # Memastikan hanya satu thread yang bisa mengakses stok sekaligus
        try:
            # Baca stok
            with open(STOCK_FILE, 'r') as f:
                stock_data = f.read().strip()

            if not stock_data.isdigit():
                return "Stock file corrupted or unreadable", 500

            stock = int(stock_data)

            # Cek apakah stok cukup
            if stock < qty:
                return f"Insufficient stock! Available: {stock}", 400

            # Kurangi stok
            stock -= qty

            # Tulis kembali stok yang sudah dikurangi
            with open(STOCK_FILE, 'w') as f:
                f.write(str(stock))

            return f"Successfully bought {qty} {item}(s). Remaining: {stock}"
        
        except Exception as e:
            return f"Internal error: {e}", 500

if __name__ == '__main__':
    # Inisialisasi stok
    with open(STOCK_FILE, 'w') as f:
        f.write('10')  # Set stok awal ke 10

    app.run(debug=True, threaded=True)
