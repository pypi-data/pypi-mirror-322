"""Prompt class for generating prompts"""


class Prompts:
    """Class for generating prompts"""

    @staticmethod
    def get_tags_prompt(transcribed_and_diarized: str) -> tuple:
        """
        Generate a prompt for getting tags from OpenAI.

        Parameters
        ----------
        transcribed_and_diarized : str
            The transcribed and diarized conversation.

        Returns
        -------
        tuple
            A tuple containing the system message and user message.
        """
        system_message = "You are a helpful analysis of transactional sales data."
        user_message = f"Return a comma-separated list of maximum five tags for the following conversation. \n\n Conversation: {transcribed_and_diarized}"
        return system_message, user_message

    @staticmethod
    def summarize_conversation_prompt(transcribed_and_diarized: str) -> tuple:
        """
        Generate a prompt for summarizing a conversation.

        Parameters
        ----------
        transcribed_and_diarized : str
            The transcribed and diarized conversation.

        Returns
        -------
        tuple
            A tuple containing the system message and user message.
        """
        system_message = "You are a helpful assistant for summarizing conversations."
        user_message = f"Summarize the following conversation in a concise manner. Clearly state the objectives for all speakers. \n\n Conversation: {transcribed_and_diarized}"

        user_message = f"""
            Your task is to create a summary of the presented conversation. If possible, the summary should include:
                - The reason for the customer's contact with support.
                - A brief description of the resolution process and the outcome.
                - The company's products and any offers made by the operator to the customer.
                - A one-sentence evaluation of the customer's satisfaction.

            Conversely, the summary should not include:
                - Personal information of the customer and operator (e.g., names, addresses).
                - Greetings exchanged between the customer and operator.

            Ensure that the summary contains only information that can be found in the text, taking care not to introduce any new information. Write the summary in the Slovak language. Formatting instructions:
            {transcribed_and_diarized}"""
        return system_message, user_message

    @staticmethod
    def get_sentiment_score_prompt(transcribed_and_diarized: str) -> tuple:
        """
        Generate a prompt for getting the sentiment score of a conversation.

        Parameters
        ----------
        transcribed_and_diarized : str
            The transcribed and diarized conversation.

        Returns
        -------
        tuple
            A tuple containing the system message and user message.
        """
        system_message = (
            "Provide a floating-point representation of the sentiment of "
            + "the following customer product review that is "
            + "rounded to five decimal places. "
            + "The scale ranges from -1.0 (negative) to 1.0 (positive) "
            + "where 0.0 represents neutral sentiment. "
            + "Only return the sentiment score value and nothing else. "
            + "You may only return a single numeric value."
        )
        user_message = f"Conversation: {transcribed_and_diarized}"
        return system_message, user_message
