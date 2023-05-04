from py2neo import Graph, Node, Relationship
import logging


class Neo4jManager:
    def __init__(self, uri="neo4j://localhost:7687", user="neo4j", password="admin123"):
        try:
            self.driver = Graph(uri, auth=(user, password))
        except Exception as e:
            logging.error(f"Cannot connect to neo4j, err= {e}")

    def query(self, query, parameters=None, db=None):
        response = None
        try:
            # session = self.driver.run(database=db) if db is not None else self.driver.session()
            response = list(self.driver.run(query, parameters))
        except Exception as e:
            logging.error(f"Cannot to execute the query {query}, err= {e}")
        finally:
            pass

        return response

    def create_VKnode(self, value):

        if value['is_closed']:
            person = Node("Person", **value)
            self.driver.create()
            return 0

        person = Node("Person", id=value["id"], nickname=value["nickname"], bdate=value["bdate"],
                      music=value["music"], university=value["university"], university_name=value["university_name"],
                      faculty=value["faculty"], faculty_name=value["faculty_name"], graduation=value["graduation"],
                      sex=value["sex"], name=value["first_name"], last_name=value["last_name"],
                      can_access_closed=value["can_access_closed"], is_closed=value["is_closed"])
        self.driver.merge(person, "Person", "id")

        city = Node("City", id=value["city"]["id"], name=value["city"]["title"])
        self.driver.merge(city, "City", "id")

        city_of = Relationship(person, "city", city)
        self.driver.merge(city_of, "City", "id")

        country = Node("Country", id=value["country"]["id"], title=value["country"]["title"])
        self.driver.merge(country, "Country", "id")

        country_of = Relationship(person, "country", country)
        self.driver.merge(country_of, "Country", "id")

        schools = value["schools"]
        for s in schools:
            school = Node("School", id=s["id"], name=s["name"],
                          year_from=s["year_from"], year_to=s["year_to"], year_graduated=s.get("year_graduated"))
            self.driver.merge(school, "School", "id")

            school_of = Relationship(person, "school", school)

            self.driver.merge(school_of, "School", "id")

        return 0
