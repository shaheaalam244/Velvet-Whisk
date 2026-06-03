import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from datetime import datetime
from models import db, User, Cake, Cart, Wishlist, Order, OrderItem, CustomOrder
from config import Config


# ---------------- APP FACTORY ----------------
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # ---------------- HOME PAGE ----------------
    @app.route('/')
    def home():
        flavour = request.args.get('flavour')
        if flavour:
            cakes = Cake.query.filter(Cake.flavour.ilike(f"%{flavour}%")).all()
        else:
            cakes = Cake.query.all()
        return render_template('index.html', cakes=cakes)

    # ---------------- REGISTER ----------------
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']

            if User.query.filter_by(email=email).first():
                flash('Email already exists!', 'danger')
                return redirect(url_for('register'))

            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('Account created! Please login.', 'success')
            return redirect(url_for('login'))
        return render_template('register.html')

    # ---------------- LOGIN ----------------
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']

            user = User.query.filter_by(email=email).first()
            if user and user.check_password(password):
                login_user(user)
                flash('Logged in successfully!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Invalid credentials!', 'danger')
        return render_template('login.html')

    # ---------------- LOGOUT ----------------
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('Logged out successfully!', 'info')
        return redirect(url_for('home'))

    # ---------------- ADD TO CART ----------------
    @app.route('/add_to_cart/<int:cake_id>')
    @login_required
    def add_to_cart(cake_id):
        item = Cart(user_id=current_user.id, cake_id=cake_id)
        db.session.add(item)
        db.session.commit()
        flash('🎂 Cake added to cart!', 'success')
        return redirect(url_for('home'))

    # ---------------- VIEW CART ----------------
    @app.route('/cart')
    @login_required
    def view_cart():
        items = Cart.query.filter_by(user_id=current_user.id).all()
        total = sum(item.cake.price for item in items)
        return render_template('cart.html', items=items, total=total)

    # ---------------- REMOVE FROM CART ----------------
    @app.route('/remove_cart/<int:item_id>')
    @login_required
    def remove_cart(item_id):
        item = Cart.query.get_or_404(item_id)
        if item.user_id == current_user.id:
            db.session.delete(item)
            db.session.commit()
            flash("🗑️ Item removed from cart.", "info")
        return redirect(url_for('view_cart'))

    # ---------------- ADD TO WISHLIST ----------------
    @app.route('/add_to_wishlist/<int:cake_id>')
    @login_required
    def add_to_wishlist(cake_id):
        item = Wishlist(user_id=current_user.id, cake_id=cake_id)
        db.session.add(item)
        db.session.commit()
        flash("💖 Added to wishlist!", "success")
        return redirect(url_for('home'))

    # ---------------- VIEW WISHLIST ----------------
    @app.route('/wishlist')
    @login_required
    def view_wishlist():
        items = Wishlist.query.filter_by(user_id=current_user.id).all()
        return render_template('wishlist.html', items=items)

    # ---------------- REMOVE FROM WISHLIST ----------------
    @app.route('/remove_wishlist/<int:item_id>')
    @login_required
    def remove_wishlist(item_id):
        item = Wishlist.query.get_or_404(item_id)
        if item.user_id == current_user.id:
            db.session.delete(item)
            db.session.commit()
            flash("💔 Item removed from wishlist.", "info")
        return redirect(url_for('view_wishlist'))

    # ---------------- CHECKOUT ----------------
    @app.route('/checkout', methods=['GET', 'POST'])
    @login_required
    def checkout():
        items = Cart.query.filter_by(user_id=current_user.id).all()
        total = sum(item.cake.price for item in items)
        if request.method == 'POST':
            address = request.form['address']
            city = request.form['city']
            pincode = request.form['pincode']

            new_order = Order(
                user_id=current_user.id,
                total_amount=total,
                address=address,
                city=city,
                pincode=pincode
            )
            db.session.add(new_order)
            db.session.commit()

            for item in items:
                order_item = OrderItem(
                    order_id=new_order.id,
                    cake_id=item.cake_id,
                    quantity=item.quantity
                )
                db.session.add(order_item)
                db.session.delete(item)
            db.session.commit()

            flash("✅ Order placed successfully!", "success")
            return redirect(url_for("payment_page", order_id=new_order.id))
        return render_template('checkout.html', items=items, total=total)

    # ---------------- PAYMENT PAGE ----------------
    @app.route('/payment/<int:order_id>')
    @login_required
    def payment_page(order_id):
        order = Order.query.get_or_404(order_id)
        return render_template('payment.html', order=order)

    # ---------------- PAYMENT SUCCESS ----------------
    @app.route('/payment_success/<int:order_id>')
    @login_required
    def payment_success(order_id):
        order = Order.query.get_or_404(order_id)
        order.status = "Paid"
        db.session.commit()
        flash("💸 Payment successful! Your order is being processed.", "success")
        return redirect(url_for('home'))

    # ---------------- CUSTOM ORDER ----------------
    @app.route('/custom_order', methods=['GET', 'POST'])
    @login_required
    def custom_order():
        if request.method == 'POST':
            message = request.form['message']
            image = request.files['image']

            if image and image.filename != '':
                filename = secure_filename(image.filename.replace(" ", "_"))
                upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(upload_path)
                rel_path = f"uploads/{filename}".replace("\\", "/")


                custom_order = CustomOrder(
                    user_id=current_user.id,
                    message=message,
                    image_path=rel_path
                )
                db.session.add(custom_order)
                db.session.commit()
                flash('🎨 Custom cake request sent successfully!', 'success')
                return redirect(url_for('home'))
            else:
                flash("⚠️ Please upload an image!", "warning")

        return render_template('custom_order.html')

    # ---------------- ADMIN ADD CAKE ----------------
    @app.route('/admin_add_cake', methods=['GET', 'POST'])
    @login_required
    def admin_add_cake():
        if current_user.username != "admin":
            flash("Access denied!", "danger")
            return redirect(url_for("home"))

        if request.method == 'POST':
            name = request.form['name']
            flavour = request.form['flavour']
            price = request.form['price']
            weight = request.form['weight']
            description = request.form['description']
            image = request.files['image']

            image_path = "images/default_cake.jpg"
            if image and image.filename != '':
                filename = secure_filename(image.filename.replace(" ", "_"))
                upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(upload_path)

            # ✅ store relative path only
                image_path = f"uploads/{filename}"

            cake = Cake(
                name=name,
                flavour=flavour,
                price=price,
                weight=weight,
                description=description,
                image_path=image_path
            )
            db.session.add(cake)
            db.session.commit()
            flash(f"✅ '{name}' added successfully!", "success")
            return redirect(url_for('admin_dashboard'))

        return render_template('admin_add_cake.html')

    # ---------------- ADMIN DASHBOARD ----------------
    @app.route('/admin_dashboard')
    @login_required
    def admin_dashboard():
        if current_user.username != "admin":
            flash("Access denied!", "danger")
            return redirect(url_for("home"))

        users = User.query.all()
        orders = Order.query.all()
        custom_orders = CustomOrder.query.all()
        cakes = Cake.query.all()
        return render_template('admin_dashboard.html', users=users, orders=orders, custom_orders=custom_orders, cakes=cakes)

    # ---------------- ADMIN CONFIRM/CANCEL ORDER ----------------
    @app.route("/confirm_order/<int:order_id>")
    @login_required
    def confirm_order(order_id):
        if current_user.username != "admin":
            flash("Access denied!", "danger")
            return redirect(url_for("home"))
        order = Order.query.get_or_404(order_id)
        order.status = "Confirmed"
        db.session.commit()
        flash(f"✅ Order #{order.id} confirmed!", "success")
        return redirect(url_for("admin_dashboard"))

    @app.route("/cancel_order/<int:order_id>")
    @login_required
    def cancel_order(order_id):
        if current_user.username != "admin":
            flash("Access denied!", "danger")
            return redirect(url_for("home"))
        order = Order.query.get_or_404(order_id)
        order.status = "Cancelled"
        db.session.commit()
        flash(f"❌ Order #{order.id} cancelled!", "info")
        return redirect(url_for("admin_dashboard"))

    # ---------------- DELETE CAKE ----------------
    @app.route('/delete_cake/<int:cake_id>')
    @login_required
    def delete_cake(cake_id):
        if current_user.username != "admin":
            flash("Access denied!", "danger")
            return redirect(url_for("home"))

        cake = Cake.query.get_or_404(cake_id)
        db.session.delete(cake)
        db.session.commit()
        flash(f"🗑️ '{cake.name}' deleted successfully!", "info")
        return redirect(url_for("admin_dashboard"))

    return app


# ---------------- RUN APP ----------------
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
