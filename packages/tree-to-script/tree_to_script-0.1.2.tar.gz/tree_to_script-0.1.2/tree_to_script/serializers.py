from abc import ABC, abstractmethod
import shlex

class CommandSerializer(ABC):
    @abstractmethod
    def serialize(self, commands):
        """Convert commands list to string format"""
        pass

    @abstractmethod
    def deserialize(self, content):
        """Parse string format back to commands list"""
        pass

class BashArraySerializer(CommandSerializer):
    def serialize(self, commands):
        # Quote the commands if they aren't already quoted
        quoted_commands = [
            cmd if cmd.startswith("'") and cmd.endswith("'")
            else shlex.quote(cmd)
            for cmd in commands
        ]
        lines = ["commands=("]
        lines.extend(f"  {cmd}" for cmd in quoted_commands)
        lines.append(")")
        return "\n".join(lines)

    def deserialize(self, content):
        lines = content.strip().splitlines()
        if lines[0] == "commands=(" and lines[-1] == ")":
            # Strip any quotes from the commands when deserializing
            return [
                line.strip().strip("'\"")
                for line in lines[1:-1]
                if line.strip()
            ]
        return []


class YamlSerializer(CommandSerializer):
    def serialize(self, commands):
        lines = ["commands:"]
        lines.extend(f"  - {cmd}" for cmd in commands)
        return "\n".join(lines)

    def deserialize(self, content):
        lines = content.strip().splitlines()
        if lines[0] == "commands:":
            return [line[4:].strip() for line in lines[1:] if line.strip()]
        return []
