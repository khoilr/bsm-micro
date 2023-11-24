from tortoise.exceptions import DoesNotExist
from typing import List, Union
from database.models.person import PersonModel


class PersonDAO:
    @staticmethod
    async def get(person_id: int) -> Union[PersonModel, None]:
        """
        Retrieve a specific Person by its ID.

        Args:
            person_id (int): Person id

        Returns:
            Union[PersonModel, None]: Person model or None if not found
        """
        try:
            return await PersonModel.get(person_id=person_id)
        except DoesNotExist:
            return None

    @staticmethod
    async def get_all() -> List[PersonModel]:
        """
        Retrieve all Persons.

        Returns:
            List[PersonModel]: List of person models
        """
        return await PersonModel.all()

    @staticmethod
    async def filter(**kwargs) -> List[PersonModel]:
        """
        Filter Persons based on provided keyword arguments.

        Returns:
            List[PersonModel]: List of person models
        """
        return await PersonModel.filter(**kwargs)

    @staticmethod
    async def create(**kwargs) -> PersonModel:
        """
        Create a new Person using provided keyword arguments.

        Returns:
            PersonModel: Person model
        """
        return await PersonModel.create(**kwargs)

    @staticmethod
    async def update(person_id: int, **kwargs):
        """
        Update a specific Person using provided keyword arguments.

        Args:
            person_id (int): Person id
        """
        person = await PersonDAO.get(person_id)
        if person:
            updatedPerson = await person.update_from_dict(kwargs)
            await updatedPerson.save()
            return updatedPerson
        return None

    @staticmethod
    async def delete(person_id: int):
        """
        Delete a specific Person by its ID.

        Args:
            person_id (int): Person id
        """
        person = await PersonDAO.get(person_id)
        if person:
            await person.delete()
            return person
        return None

    @staticmethod
    def model_to_json(person: PersonModel) -> dict:
        """
        Convert PersonModel instance to JSON string.

        Args:
            person (PersonModel): Person model

        Returns:
            dict: Model data as JSON key-value datatype
        """
        return person.to_json()
