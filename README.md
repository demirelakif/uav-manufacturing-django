# :small_airplane: UAV Manufacturing System

UAV Manufacturing System is a Django-based web application designed for managing unmanned aerial vehicles (UAVs) and associated parts. This project allows users to produce and manage both UAVs and parts, track inventory, and assign roles to staff members. The system supports seamless interactions between different teams (like assembly teams and part production teams) and provides real-time data updates.

## 🚀 Features

- **User Authentication:** Secure login/logout for different user roles.
- **Team-based Access Control:** Different teams (e.g., aircraft assembly team, part production team) have specific permissions.
- **Inventory Management:** View and manage parts and aircrafts, including stock levels.
- **Staff Management:** View team members and their respective roles.
- **Part Deletion:** Users can delete parts by specifying the quantity.
- **Real-time Updates:** The application uses AJAX and DataTables for a smooth user experience.

## :man_technologist: Technologies Used

<div>
	<code><img width="50" src="https://user-images.githubusercontent.com/25181517/202896760-337261ed-ee92-4979-84c4-d4b829c7355d.png" alt="Tailwind CSS" title="Tailwind CSS"/></code>
	<code><img width="50" src="https://user-images.githubusercontent.com/25181517/186711335-a3729606-5a78-4496-9a36-06efcc74f800.png" alt="Swagger" title="Swagger"/></code>
	<code><img width="50" src="https://github.com/marwin1991/profile-technology-icons/assets/62091613/9bf5650b-e534-4eae-8a26-8379d076f3b4" alt="Django" title="Django"/></code>
	<code><img width="50" src="https://user-images.githubusercontent.com/25181517/117208740-bfb78400-adf5-11eb-97bb-09072b6bedfc.png" alt="PostgreSQL" title="PostgreSQL"/></code>
	<code><img width="50" src="https://user-images.githubusercontent.com/25181517/117207330-263ba280-adf4-11eb-9b97-0ac5b40bc3be.png" alt="Docker" title="Docker"/></code>
</div>
<br/>

- **Django:** Web framework for Python.
- **PostgreSQL:** Database management.
- **Docker:** Containerization for easy deployment and scalability.
- **Bootstrap & Tailwind CSS:** For responsive and modern UI.
- **jQuery & DataTables:** For dynamic data tables and AJAX calls.

## 🖥️ Setup Instructions

### Clone the repository:

```bash
git clone https://github.com/your-username/uav-rental.git
cd uav-rental
````

### Install dependencies:
```bash
pip install -r requirements.txt
````

### Set up the database:
```bash
python manage.py migrate
python manage.py loaddata fixtures/initial_teams.json
python manage.py collectstatic
````

### Run the server:
```bash
python manage.py runserver
````

## Docker Setup
To run the application in a Docker container:

### Build the Docker image:
```bash
docker build -t uav-manufacturing .
````

### Run the Docker container:
```bash
docker run -p 8000:8000 uav-manufacturing
````
Access the app at http://localhost:8000.

## :film_strip: Screenshots

### Swagger Docs

![uav6](https://github.com/user-attachments/assets/dbb5a2f6-5f7a-4991-b4b4-bef3be2cb52a)

### Register

![uav-3](https://github.com/user-attachments/assets/e7dc2a5c-7686-4c0e-bd71-69cdbb38f318)

### Dashboard

![uav-1](https://github.com/user-attachments/assets/195c4a3c-5f46-43b6-8885-1f4462a0b7b6)

### Produce Part

![uav-2](https://github.com/user-attachments/assets/56ebd410-cb61-4cde-b0bd-4bf898b53d41)

### Produce Aircraft(UAV)

![uav4](https://github.com/user-attachments/assets/0bc40fc6-ca58-4765-8475-cb74ac2a1575)




