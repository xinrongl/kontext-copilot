from abc import abstractmethod

from kontext_copilot.copilot._session import CopilotSession
from kontext_copilot.data.schemas import (
    ChatRoles,
    CreateSessionMessageModel,
    SessionMessageModel,
)
from kontext_copilot.utils import get_logger


class BaseTool:
    def __init__(self, tool_name: str, session: CopilotSession) -> None:
        self.tool_name = tool_name
        self.session = session
        self._logger = get_logger()
        self._initialise()

    def _initialise(self):
        """
        Initialise the tool
        """
        self.data_source = self.session.data_source
        self.data_provider = self.session.data_provider

    @abstractmethod
    def execute(self, **kwargs):
        pass

    def add_message(
        self,
        message: str,
        role: ChatRoles = ChatRoles.SYSTEM,
        is_system_prompt: bool = False,
        is_streaming: bool = False,
        copilot_generated: bool = True,
        generating: bool = True,
    ) -> SessionMessageModel:
        """
        Add a new message to the session
        """
        message_model = CreateSessionMessageModel(
            session_id=self.session.session_id,
            message=message,
            role=role,
            is_system_prompt=is_system_prompt,
            is_streaming=is_streaming,
            copilot_generated=copilot_generated,
            generating=generating,
        )
        return self.session.session_service.add_session_message(
            self.session.session_id, message_model
        )

    def append_message_part(
        self, message_id: int, message_part: str, done: bool = False
    ) -> SessionMessageModel:
        """
        Append a message part to the message
        """
        return self.session.session_service.append_message_part(
            self.session.session_id, message_id, message_part, done
        )

    def append_new_line(
        self, message_id: int, done: bool = False
    ) -> SessionMessageModel:
        """
        Append a new line to the message
        """
        return self.append_message_part(message_id, "\n", done)