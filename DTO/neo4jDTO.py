from py2neo import Graph, Node, Relationship
import logging

from DTO.kafkaDTO import KafkaConsumerManager


class Neo4jManager:
    def __init__(self, uri="neo4j://localhost:7687", user="neo4j", password="admin123"):
        try:
            self.driver = Graph(uri, auth=(user, password))
        except Exception as e:
            logging.error(f"Cannot connect to neo4j, err= {e}")

    def query(self, query, parameters=None):
        response = None
        try:
            response = list(self.driver.run(query, parameters))
        except Exception as e:
            logging.error(f"Cannot to execute the query {query}, err= {e}")
        finally:
            pass

        return response

    def create_vk_user(self, value):
        logging.info(f"create the User node for {value['id']}")
        tx = self.driver.begin()
        try:
            city, country, schools = None, None, None

            if value.get("city"):
                city = value.pop("city")

            if value.get("country"):
                country = value.pop("country")

            if value.get("schools"):
                schools = value.pop("schools")

            person = Node(name=value.pop("first_name"), **value)

            tx.merge(person, "Person", "id")

            if city:
                city = Node("City", id=city["id"], name=city["title"])
                tx.merge(city, "City", "id")

                city_of = Relationship(person, "city", city)
                tx.merge(city_of, "City", "id")

            if country:
                country = Node("Country", id=country["id"], title=country["title"])
                tx.merge(country, "Country", "id")

                country_of = Relationship(person, "country", country)
                tx.merge(country_of, "Country", "id")

            if schools:
                for s in schools:
                    school = Node("School", **s)
                    tx.merge(school, "School", "id")

                    school_of = Relationship(person, "school", school)

                    tx.merge(school_of, "School", "id")

            tx.commit()
        except Exception as e:
            tx.rollback()
            logging.error(f"Something going wrong in vk_user, err={e}, \n value = {value}")
        return 0

    def create_friends_relation(self, user_id, friends_id):
        try:
            logging.info(f"Transfers friends of {user_id}")
            query = "MERGE (a:Person { id: $user_id })" \
                    "MERGE (b:Person { id: $friend_id })" \
                    "CREATE (a)-[:FRIENDS]->(b)"
            for friend_id in friends_id:
                response = self.query(query, {"user_id": user_id, "friend_id": friend_id})
        except Exception as e:
            logging.error(f"There is an error at {user_id} user_id, err={e}")




