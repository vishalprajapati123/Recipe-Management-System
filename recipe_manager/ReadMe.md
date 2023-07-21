# RecipeApp

RecipeApp is a web application that allows users to create, view, and rate recipes.

## Setting up the project locally

1. Navigate to the root directory of the project where `manage.py` is located.

   ```
   virtualenv venv
   source venv/bin/activate
   ```
2. Now, install the required dependencies:

   ```
   pip install -r requirements.txt
   ```
3. Run the following commands to apply database migrations:

   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```
4. To create a superuser for the Django admin site, run:

   ```sh
   python manage.py createsuperuser
   ```

   Follow the prompts to set a username, email, and password for the superuser.
5. You can now run the Django development server with:

   ```sh
   python manage.py runserver
   ```
6. For running test cases

   ```
   python manage.py test recipes.tests.test_views

   ```
7. Access the Django admin site by navigating to `http://localhost:8000/admin` and logging in with the superuser credentials.

## Setting up the project using Docker

1. Make sure you have Docker and Docker Compose installed on your system.
2. Navigate to the root directory of the project where the `docker-compose.yml` file is located.
3. Build and start the Docker containers using the following command:

   ```sh
   docker-compose up --build 
   ```
4. Run migrations to set up the database:

   ```sh
   docker-compose exec web python manage.py makemigrations
   docker-compose exec web python manage.py migrate
   ```
5. Create a superuser to access the Django admin site:

   ```sh
   docker-compose exec web python manage.py createsuperuser
   ```

   Follow the prompts to set a username, email, and password for the superuser.
6. For running test cases

   ```
   docker-compose exec web python manage.py test recipes.tests.test_views

   ```
7. The application should now be running at `http://localhost:8000`.
8. Access the Django admin site by navigating to `http://localhost:8000/admin` and logging in with the superuser credentials.

## API Documentation

RecipeApp provides a RESTful API for creating, retrieving, and rating recipes. Below is the documentation for the API endpoints:

### User Endpoints

- `POST /register/`

  - Register a new user.
  - Required fields: `username`, `email`, `password`.
- `POST /login/`

  - Authenticate an existing user.
  - Required fields: `username`, `password`.

### Recipe Endpoints

* ` /recipes/`

- `GET /recipes/`

  - Retrieve a list of all recipes.
- `POST /recipes/`

  - Create a new recipe.
  - Required fields: `title`, `description`,`ingredients`, `instructions`.
  - Must be authenticated.
- `GET /recipes/<int:pk>/`

  - Retrieve details of a specific recipe by its ID.
- `PUT /recipes/<int:pk>/`

  - Update details of a specific recipe by its ID.
- `DELETE /recipes/<int:pk>/`
- Retrieve details of a specific recipe by its ID.

### Rating Endpoint

- `POST /rating/`
  - Rate a recipe.
  - Required fields: `recipe`, `rating`.
  - Must be authenticated.

### Search Endpoint

- `GET /search/`
  - Search for recipes by title or ingredients.
  - Use query parameters to specify the search, e.g. `/search/?title=soup`.

Note: Endpoints that create or rate recipes require the user to be authenticated.
