
CREATE TABLE suppliers (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(200) NOT NULL,
    contact_person VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(100),
    address TEXT,
    payment_terms VARCHAR(100),
    currency ENUM('USD', 'ZWL', 'RAND'),
    notes TEXT,
    date_created DATETIME,
    PRIMARY KEY (id)
);

CREATE TABLE customers (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(200) NOT NULL,
    identification_number VARCHAR(50),
    citizenship VARCHAR(100),
    address TEXT,
    phone VARCHAR(20),
    email VARCHAR(100),
    date_created DATETIME,
    PRIMARY KEY (id)
);

CREATE TABLE inventory (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(200) NOT NULL,
    brand VARCHAR(100),
    category VARCHAR(100),
    specifications TEXT,
    quantity INTEGER,
    unit_price FLOAT NOT NULL,
    currency ENUM('USD', 'ZWL', 'RAND'),
    supplier_id INTEGER,
    payment_type ENUM('CASH', 'ECOCASH', 'SWIPE', 'TRANSFER', 'CREDIT'),
    minimum_stock_level INTEGER,
    notes TEXT,
    date_created DATETIME,
    date_updated DATETIME,
    PRIMARY KEY (id),
    FOREIGN KEY(supplier_id) REFERENCES suppliers (id)
);

CREATE TABLE activity_types (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    is_active BOOLEAN,
    date_created DATETIME,
    PRIMARY KEY (id),
    UNIQUE (name)
);

CREATE TABLE activities (
    id INT NOT NULL AUTO_INCREMENT,
    customer_id INTEGER NOT NULL,
    activity_type_id INTEGER NOT NULL,
    description TEXT NOT NULL,
    status ENUM('SCHEDULED', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED'),
    date DATE NOT NULL,
    completed_date DATE,
    technician VARCHAR(100),
    equipment_used TEXT,
    labor_hours FLOAT,
    labor_cost FLOAT,
    material_cost FLOAT,
    total_cost FLOAT,
    currency ENUM('USD', 'ZWL', 'RAND'),
    notes TEXT,
    date_created DATETIME,
    PRIMARY KEY (id),
    FOREIGN KEY(customer_id) REFERENCES customers (id),
    FOREIGN KEY(activity_type_id) REFERENCES activity_types (id)
);

CREATE TABLE invoices (
    id INT NOT NULL AUTO_INCREMENT,
    customer_id INTEGER NOT NULL,
    total_amount FLOAT NOT NULL,
    currency ENUM('USD', 'ZWL', 'RAND'),
    tax_amount FLOAT,
    discount_amount FLOAT,
    status ENUM('PENDING', 'PAID', 'OVERDUE', 'CANCELLED'),
    due_date DATE,
    paid_date DATE,
    payment_method ENUM('CASH', 'ECOCASH', 'SWIPE', 'TRANSFER', 'CREDIT'),
    notes TEXT,
    date_created DATETIME,
    PRIMARY KEY (id),
    FOREIGN KEY(customer_id) REFERENCES customers (id)
);

CREATE TABLE invoice_items (
    id INT NOT NULL AUTO_INCREMENT,
    invoice_id INTEGER NOT NULL,
    inventory_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price FLOAT NOT NULL,
    description TEXT,
    PRIMARY KEY (id),
    FOREIGN KEY(invoice_id) REFERENCES invoices (id),
    FOREIGN KEY(inventory_id) REFERENCES inventory (id)
);

CREATE TABLE stock_transactions (
    id INT NOT NULL AUTO_INCREMENT,
    inventory_id INTEGER NOT NULL,
    transaction_type ENUM('STOCK_IN', 'STOCK_OUT', 'ADJUSTMENT') NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price FLOAT,
    total_value FLOAT,
    currency ENUM('USD', 'ZWL', 'RAND'),
    reason ENUM('SOLD_TO_CUSTOMER', 'INSTALLED_TO_CLIENT', 'DAMAGED', 'RETURNED', 'ADJUSTMENT'),
    reference_id INTEGER,
    reference_type VARCHAR(50),
    customer_name VARCHAR(200),
    notes TEXT,
    created_by VARCHAR(100),
    date_created DATETIME,
    PRIMARY KEY (id),
    FOREIGN KEY(inventory_id) REFERENCES inventory (id)
);

CREATE TABLE financial_records (
    id INT NOT NULL AUTO_INCREMENT,
    type ENUM('INCOME', 'EXPENSE') NOT NULL,
    category VARCHAR(100),
    description TEXT NOT NULL,
    amount FLOAT NOT NULL,
    currency ENUM('USD', 'ZWL', 'RAND'),
    date DATE NOT NULL,
    payment_method ENUM('CASH', 'ECOCASH', 'SWIPE', 'TRANSFER', 'CREDIT'),
    receipt_number VARCHAR(100),
    vendor_supplier VARCHAR(200),
    reference_id INTEGER,
    notes TEXT,
    date_created DATETIME,
    PRIMARY KEY (id)
);

CREATE TABLE custom_fields (
    id INT NOT NULL AUTO_INCREMENT,
    entity_type VARCHAR(50) NOT NULL,
    entity_id INTEGER NOT NULL,
    field_name VARCHAR(100) NOT NULL,
    field_value TEXT,
    field_type VARCHAR(20),
    date_created DATETIME,
    PRIMARY KEY (id)
);

CREATE TABLE financial_categories (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    type ENUM('INCOME', 'EXPENSE') NOT NULL,
    description TEXT,
    is_active BOOLEAN,
    date_created DATETIME,
    PRIMARY KEY (id)
);

CREATE TABLE locations (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    address TEXT,
    latitude FLOAT,
    longitude FLOAT,
    category ENUM('CUSTOMER', 'SUPPLIER', 'SERVICE', 'OFFICE', 'OTHER'),
    visit_frequency INTEGER,
    last_visit DATETIME,
    notes TEXT,
    date_created DATETIME,
    PRIMARY KEY (id)
);

CREATE TABLE pricing (
    id INT NOT NULL AUTO_INCREMENT,
    item_type VARCHAR(50) NOT NULL,
    item_name VARCHAR(100) NOT NULL,
    price FLOAT NOT NULL,
    currency ENUM('USD', 'ZWL', 'RAND'),
    unit VARCHAR(20),
    effective_date DATETIME,
    expiry_date DATETIME,
    notes TEXT,
    date_created DATETIME,
    PRIMARY KEY (id)
);

CREATE TABLE fuel_records (
    id INT NOT NULL AUTO_INCREMENT,
    journey_id INTEGER,
    vehicle_id INTEGER,
    fuel_type ENUM('PETROL', 'DIESEL', 'LPG', 'ELECTRIC'),
    liters FLOAT,
    total_cost FLOAT,
    currency ENUM('USD', 'ZWL', 'RAND'),
    odometer_reading FLOAT,
    date DATE NOT NULL,
    notes TEXT,
    date_created DATETIME,
    PRIMARY KEY (id),
    FOREIGN KEY(journey_id) REFERENCES journey_records (id)
);

CREATE TABLE mileage_records (
    id INT NOT NULL AUTO_INCREMENT,
    journey_id INTEGER,
    vehicle_id INTEGER,
    start_location VARCHAR(100),
    end_location VARCHAR(100),
    distance_km FLOAT,
    start_odometer FLOAT,
    end_odometer FLOAT,
    date DATE NOT NULL,
    notes TEXT,
    date_created DATETIME,
    PRIMARY KEY (id),
    FOREIGN KEY(journey_id) REFERENCES journey_records (id)
);

CREATE TABLE journey_records (
    id INT NOT NULL AUTO_INCREMENT,
    activity_id INTEGER,
    vehicle_id INTEGER,
    driver VARCHAR(100),
    start_location VARCHAR(100),
    end_location VARCHAR(100),
    start_time DATETIME,
    end_time DATETIME,
    purpose VARCHAR(200),
    status ENUM('PLANNED', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED'),
    total_distance FLOAT,
    total_fuel_cost FLOAT,
    notes TEXT,
    date_created DATETIME,
    PRIMARY KEY (id),
    FOREIGN KEY(activity_id) REFERENCES activities (id)
);
