from pydantic import BaseModel, ValidationError
from pydantic import NonNegativeInt, model_validator, Field
import shutil
from typing import Any, cast


class check(BaseModel):
    """
    Pydantic model for validating the maze configuration parameters.
    """
    WIDTH: int = Field(ge=9, le=238)
    HEIGHT: int = Field(ge=7, le=238)
    ENTRY: tuple[NonNegativeInt, NonNegativeInt]
    EXIT: tuple[NonNegativeInt, NonNegativeInt]
    OUTPUT_FILE: str
    PERFECT: bool = True

    @model_validator(mode="after")
    def customvalidation(self) -> check:
        """
        Performs cross-field validation for entry/exit coordinates and bounds.

        Returns:
            check: The validated model instance.
        Raises:
            ValueError: If entry/exit are outside bounds or identical.
        """
        if self.ENTRY[0] >= self.WIDTH or self.ENTRY[1] >= self.HEIGHT:
            raise ValueError("Entry point should be inside maze")
        if self.EXIT[0] >= self.WIDTH or self.EXIT[1] >= self.HEIGHT:
            raise ValueError("EXIT point should be inside maze")
        if self.EXIT[0] == self.ENTRY[0] and self.EXIT[1] == self.ENTRY[1]:
            raise ValueError("The starting point cannot be the "
                             "same as the ending point.")
        return self


config: dict[str, Any] = {}


def ret_check(config_file: str) -> dict[str, Any]:
    """
    Reads, parses, and validates the maze configuration from a text file.

    Args:
        config_file (str): The path to the configuration text file.

    Returns:
        dict[str, Any]: A dictionary containing the validated configuration
                        parameters (WIDTH, HEIGHT, ENTRY, EXIT, PERFECT, SEED).
    """
    try:
        value: Any

        config.clear()
        with open(config_file) as oo:
            for line in oo:
                if not line or "#" in line[0]\
                   or line == "\n" or "=" not in line:
                    continue
                line = line.split("#")[0]
                key, value = map(str.strip, line.split("=", 1))
                if key in ("ENTRY", "EXIT"):
                    try:
                        value = tuple(map(int, value.replace("(", "")
                                          .replace(")", "").split(",")))
                    except ValueError:
                        print("Inputs are not a tu"
                              "ple in \"Entry\" or \"Exit\"")
                if key == "SEED":
                    try:
                        value = int(value)
                    except ValueError:
                        print("SEED must be an integer")
                        value = 0
                key = key.upper()
                if key in config:
                    raise ValueError(f" ERROR! : {key}  was placed in the "
                                     "file more than once. ")
                config[key] = value
            required_keys = {
                                "WIDTH",
                                "HEIGHT",
                                "ENTRY",
                                "EXIT",
                                "OUTPUT_FILE",
                                "PERFECT"
                            }
            config_key = set(config)
            missing = required_keys - config_key
            extra = config_key - required_keys - {"SEED"}
            error = " ERROR! in config.txt:"
            if missing:
                error = error + f"missing: {",".join(missing)}"
            if missing and extra:
                error = error + " | "
            if extra:
                error = error + f"extra: {",".join(extra)}"
            if error != " ERROR! in config.txt:":
                raise ValueError(error)
            checked = check(
                WIDTH=config["WIDTH"],
                HEIGHT=config["HEIGHT"],
                ENTRY=config["ENTRY"],
                EXIT=config["EXIT"],
                OUTPUT_FILE=config["OUTPUT_FILE"],
                PERFECT=config["PERFECT"],
                )
            ret = checked.model_dump()
            if "SEED" in config:
                try:
                    ret["SEED"] = int(config["SEED"])
                except Exception:
                    ret["SEED"] = 0
            else:
                ret["SEED"] = "None"
            width_termenal, hight_terminal = tuple(shutil.get_terminal_size())
            if (ret["HEIGHT"] * 2) + 8 > hight_terminal or\
               (ret["WIDTH"] * 4) + 1 > width_termenal:
                raise ValueError("ERROR! please enter size that"
                                 "matches the terminal dimensions..")
        return cast(dict[str, Any], ret)
    except ValidationError as e:
        for i in e.errors():
            if i["loc"]:
                print("ERROR!", str(i["loc"]).split("\'")[1],
                      "=", i["input"], ",", i["msg"])
            else:
                print("ERROR!", i["msg"])
        exit()
    except Exception as e:
        print(e)
        exit()
