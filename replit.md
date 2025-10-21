# Giebee Engineering Management System

## Overview

A comprehensive ERP (Enterprise Resource Planning) system designed for Giebee Engineering, a multi-service company specializing in solar installations, electrical work, CCTV systems, geyser installations, alarm systems, and borehole drilling. The system manages core business operations including supplier relationships, customer management, inventory control, activity tracking, invoicing, and financial record keeping. Built as a web-based application, it provides a centralized platform for managing all aspects of the engineering services business with real-time dashboards and reporting capabilities.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templating with Flask for server-side rendering
- **UI Framework**: Bootstrap 5.1.3 for responsive, mobile-first design
- **Icons**: Font Awesome 6.0.0 for consistent iconography across the interface
- **Layout Pattern**: Sidebar navigation with main content area, optimized for desktop and tablet use
- **Styling**: Custom CSS with company branding (Giebee Engineering logo and color scheme)
- **User Interface**: Card-based dashboard layout with table-driven data presentation

### Backend Architecture
- **Web Framework**: Flask (Python) following MVC pattern with route-based controllers
- **Session Management**: Flask's built-in session handling with configurable secret keys
- **PDF Generation**: ReportLab integration for invoice and report generation
- **File Handling**: In-memory file generation for downloads (PDFs, Excel files)
- **Configuration**: Environment-based configuration for database URLs and secret keys

### Data Storage Solutions
- **ORM**: SQLAlchemy with Flask-SQLAlchemy extension for database abstraction
- **Database**: Configurable backend (defaults to SQLite for development, supports PostgreSQL for production)
- **Connection Management**: Connection pooling with 300-second recycle time and health checks
- **Schema Management**: Automatic table creation via SQLAlchemy model definitions
- **Data Integrity**: Foreign key relationships and enum constraints for data consistency

### Core Business Models
- **Supplier Management**: Vendor information with contact details and payment terms
- **Customer Management**: Client database with identification, contact, and address information
- **Inventory Control**: Stock management with categories, specifications, pricing, and quantity tracking
- **Activity Tracking**: Service job management with status workflows and technician assignment
- **Invoice System**: Billing with line items, multiple currencies, and PDF generation
- **Financial Records**: Income and expense tracking with categorization and reporting
- **Stock Transactions**: Inventory movement logging with reasons and audit trails

### Business Logic Components
- **Multi-Service Support**: Handles diverse service types (solar, electrical, CCTV, borehole, etc.)
- **Currency Management**: Multi-currency support (USD, ZWL, RAND) for international operations
- **Status Workflows**: Predefined status flows for activities (Scheduled → In Progress → Completed)
- **Category Management**: Organized inventory and expense categorization for better reporting
- **Stock Control**: Low-stock alerts and automated quantity tracking with transaction history

### Security Architecture
- **Session Security**: Flask secret key configuration for session encryption
- **Environment Variables**: Secure configuration management for sensitive data
- **Input Validation**: Form validation and SQL injection protection via ORM
- **Access Control**: Basic authentication framework ready for role-based extensions

## External Dependencies

### Core Framework Dependencies
- **Flask**: Web application framework for routing and request handling
- **SQLAlchemy/Flask-SQLAlchemy**: Database ORM and Flask integration
- **ReportLab**: PDF generation library for invoices and reports

### Frontend Dependencies
- **Bootstrap 5.1.3**: CSS framework for responsive UI components
- **Font Awesome 6.0.0**: Icon library for consistent visual elements
- **jQuery**: JavaScript library for dynamic form interactions (invoice line items)

### Database Integration
- **SQLite**: Default development database (file-based)
- **PostgreSQL**: Production database option via DATABASE_URL environment variable
- **Database Drivers**: SQLite (built-in), PostgreSQL adapter for production deployments

### Environment Configuration
- **Environment Variables**: DATABASE_URL, FLASK_SECRET_KEY for deployment flexibility
- **Development Defaults**: SQLite database and fallback secret key for local development
- **Production Ready**: Configurable for cloud deployment with external databases