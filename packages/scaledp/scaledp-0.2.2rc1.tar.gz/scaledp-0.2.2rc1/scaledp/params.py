from pyspark.ml.param import Param, Params, TypeConverters
from enum import Enum

from scaledp.utils.pydantic_shema_utils import json_schema_to_model
from scaledp.langs import *
from pydantic import BaseModel
import json


class AutoParamsMeta(type(Params), type):
    def __new__(cls, name, bases, dct):
        dct_copy = dct.copy()
        for attr_name, attr_value in dct_copy.items():
            if isinstance(attr_value, Param):
                set_method_name = f"set{attr_name[0].upper()}{attr_name[1:]}"
                get_method_name = f"get{attr_name[0].upper()}{attr_name[1:]}"

                def set_method(self, value, attr_name=attr_name):
                    return self._set(**{attr_name: value})

                def get_method(self, attr_name=attr_name):
                    return self.getOrDefault(attr_name)

                dct[set_method_name] = set_method
                dct[get_method_name] = get_method

        return super(AutoParamsMeta, cls).__new__(cls, name, bases, dct)


class HasImageType(Params):

    imageType = Param(
        Params._dummy(),
        "imageType",
        "Image type.",
        typeConverter=TypeConverters.toString,
    )

    def setImageType(self, value):
        """
        Sets the value of :py:attr:`imageType`.
        """
        return self._set(imageType=value)

    def getImageType(self):
        """
        Sets the value of :py:attr:`imageType`.
        """
        return self.getOrDefault(self.imageType)


class HasKeepInputData(Params):

    keepInputData = Param(
        Params._dummy(),
        "keepInputData",
        "Keep input data column in output.",
        typeConverter=TypeConverters.toBoolean,
    )

    def setKeepInputData(self, value):
        """
        Sets the value of :py:attr:`keepInputData`.
        """
        return self._set(keepInputData=value)

    def getKeepInputData(self):
        """
        Sets the value of :py:attr:`keepInputData`.
        """
        return self.getOrDefault(self.keepInputData)


class HasPathCol(Params):
    """
    Mixin for param pathCol: path column name.
    """

    pathCol = Param(
        Params._dummy(),
        "pathCol",
        "Input column name with path of file.",
        typeConverter=TypeConverters.toString,
    )

    def setPathCol(self, value):
        """
        Sets the value of :py:attr:`pathCol`.
        """
        return self._set(pathCol=value)

    def getPathCol(self) -> str:
        """
        Gets the value of pathCol or its default value.
        """
        return self.getOrDefault(self.pathCol)


class HasInputCols(Params):
    """
    Mixin for param inputCols: input column names.
    """

    inputCols: "Param[List[str]]" = Param(
        Params._dummy(),
        "inputCols",
        "input column names.",
        typeConverter=TypeConverters.toListString,
    )

    def __init__(self) -> None:
        super(HasInputCols, self).__init__()

    def getInputCols(self):
        """
        Gets the value of inputCols or its default value.
        """
        return self.getOrDefault(self.inputCols)

    def setInputCols(self, value):
        """
        Sets the value of :py:attr:`inputCol`.
        """
        return self._set(inputCols=value)


class HasInputCol(Params):
    """
    Mixin for param inputCol: input column name.
    """

    inputCol: "Param[str]" = Param(
        Params._dummy(),
        "inputCol",
        "input column name.",
        typeConverter=TypeConverters.toString,
    )

    def __init__(self) -> None:
        super(HasInputCol, self).__init__()

    def getInputCol(self) -> str:
        """
        Gets the value of inputCol or its default value.
        """
        return self.getOrDefault(self.inputCol)

    def setInputCol(self, value):
        """
        Sets the value of :py:attr:`inputCol`.
        """
        return self._set(inputCol=value)


class HasOutputCol(Params):
    """
    Mixin for param outputCol: output column name.
    """

    outputCol: "Param[str]" = Param(
        Params._dummy(),
        "outputCol",
        "output column name.",
        typeConverter=TypeConverters.toString,
    )

    def __init__(self) -> None:
        super(HasOutputCol, self).__init__()
        self._setDefault(outputCol=self.uid + "__output")

    def getOutputCol(self) -> str:
        """
        Gets the value of outputCol or its default value.
        """
        return self.getOrDefault(self.outputCol)

    def setOutputCol(self, value):
        """
        Sets the value of :py:attr:`outputCol`.
        """
        return self._set(outputCol=value)


class HasResolution(Params):
    resolution = Param(
        Params._dummy(),
        "resolution",
        "Resolution of image.",
        typeConverter=TypeConverters.toInt,
    )

    POINTS_PER_INCH = 72

    def setResolution(self, value):
        """
        Sets the value of :py:attr:`resolution`.
        """
        return self._set(resolution=value)

    def getResolution(self):
        """
        Gets the value of :py:attr:`resolution`.
        """
        return self.getOrDefault(self.resolution)


class HasPageCol(Params):
    """
    Mixin for param pageCol: path column name.
    """

    pageCol = Param(
        Params._dummy(),
        "pageCol",
        "Page column name.",
        typeConverter=TypeConverters.toString,
    )

    def setPageCol(self, value):
        """
        Sets the value of :py:attr:`pageCol`.
        """
        return self._set(pageCol=value)

    def getPageCol(self) -> str:
        """
        Gets the value of pageCol or its default value.
        """
        return self.getOrDefault(self.pageCol)


class HasNumPartitions:
    numPartitions = Param(
        Params._dummy(),
        "numPartitions",
        "Number of partitions.",
        typeConverter=TypeConverters.toInt,
    )

    def setNumPartitions(self, value):
        """
        Sets the value of :py:attr:`numPartitions`.
        """
        return self._set(numPartitions=value)

    def getNumPartitions(self):
        """
        Gets the value of :py:attr:`numPartitions`.
        """
        return self.getOrDefault(self.numPartitions)


class HasDevice(Params):
    device = Param(Params._dummy(), "device", "Device.", typeConverter=TypeConverters.toInt)

    def setDevice(self, value):
        """
        Sets the value of :py:attr:`device`.
        """
        return self._set(device=value)

    def getDevice(self):
        """
        Gets the value of device or its default value.
        """
        return self.getOrDefault(self.device)


class HasBatchSize(Params):
    batchSize = Param(
        Params._dummy(), "batchSize", "Batch size.", typeConverter=TypeConverters.toInt
    )

    def setBatchSize(self, value):
        """
        Sets the value of :py:attr:`batchSize`.
        """
        return self._set(batchSize=value)

    def getBatchSize(self):
        """
        Gets the value of batchSize or its default value.
        """
        return self.getOrDefault(self.batchSize)


class HasWhiteList(Params):
    """
    Mixin for param whiteList.
    """

    whiteList: "Param[List[str]]" = Param(
        Params._dummy(),
        "whiteList",
        "White list.",
        typeConverter=TypeConverters.toListString,
    )

    def __init__(self) -> None:
        super(HasWhiteList, self).__init__()

    def getWhiteList(self):
        """
        Gets the value of whiteList or its default value.
        """
        return self.getOrDefault(self.whiteList)

    def setWhiteList(self, value):
        """
        Sets the value of :py:attr:`whiteList`.
        """
        return self._set(whiteList=value)


class HasBlackList(Params):
    """
    Mixin for param blackList.
    """

    blackList: "Param[List[str]]" = Param(
        Params._dummy(),
        "blackList",
        "Black list.",
        typeConverter=TypeConverters.toListString,
    )

    def getBlackList(self):
        """
        Gets the value of whiteList or its default value.
        """
        return self.getOrDefault(self.blackList)

    def setBlackList(self, value):
        """
        Sets the value of :py:attr:`blackList`.
        """
        return self._set(blackList=value)

class HasScoreThreshold(Params):
    """
    Mixin for param scoreThreshold.
    """

    scoreThreshold = Param(
        Params._dummy(),
        "scoreThreshold",
        "Score threshold.",
        typeConverter=TypeConverters.toFloat,
    )

    def __init__(self) -> None:
        super(HasScoreThreshold, self).__init__()

    def getScoreThreshold(self):
        """
        Gets the value of scoreThreshold or its default value.
        """
        return self.getOrDefault(self.scoreThreshold)

    def setScoreThreshold(self, value):
        """
        Sets the value of :py:attr:`scoreThreshold`.
        """
        return self._set(scoreThreshold=value)


class HasModel(Params):
    """
    Mixin for param model.
    """

    model = Param(Params._dummy(), "model", "Model.", typeConverter=TypeConverters.toString)

    def __init__(self) -> None:
        super(HasModel, self).__init__()

    def getModel(self):
        """
        Gets the value of model or its default value.
        """
        return self.getOrDefault(self.model)

    def setModel(self, value):
        """
        Sets the value of :py:attr:`model`.
        """
        return self._set(model=value)


class HasColor(Params):
    color = Param(Params._dummy(), "color", "Color.", typeConverter=TypeConverters.toString)

    def setColor(self, value):
        """
        Sets the value of :py:attr:`color`.
        """
        return self._set(color=value)

    def getColor(self) -> str:
        """
        Gets the value of color or its default value.
        """
        return self.getOrDefault(self.color)


class HasDefaultEnum(Params):

    @staticmethod
    def _any_lang_to_code(lang):
        if lang in TESSERACT_CODE_TO_LANGUAGE:
            return LANGUAGE_TO_CODE[TESSERACT_CODE_TO_LANGUAGE[lang]]
        elif lang in LANGUAGE_TO_CODE:
            return LANGUAGE_TO_CODE[lang]
        elif lang in CODE_TO_LANGUAGE:
            return lang
        else:
            raise ValueError(f"Invalid language: {lang}")

    def _setDefault(self, **kwargs):
        """
        Sets default params.
        """
        for param, value in kwargs.items():
            if param == "lang":
                value = [self._any_lang_to_code(lang) for lang in value]
            if value is not None and isinstance(value, Enum):
                try:
                    value = value.value
                except TypeError as e:
                    raise TypeError(
                        'Invalid default param value given for param "%s". %s' % (param, e)
                    )
            validator = "validate" + param[0].upper() + param[1:]
            if hasattr(self, validator):
                value = getattr(self, validator)(value)
            super(HasDefaultEnum, self)._setDefault(**{param: value})
        return self

    def _set(self, **kwargs):
        """
        Sets user-supplied params.
        """
        for param, value in kwargs.items():
            p = getattr(self, param)
            if value is not None:
                if p.name == "lang":
                    value = [self._any_lang_to_code(lang) for lang in value]
                if isinstance(value, Enum):
                    value = value.value
                validator = "validate" + param[0].upper() + param[1:]
                if hasattr(self, validator):
                    value = getattr(self, validator)(value)
                try:
                    value = p.typeConverter(value)
                except TypeError as e:
                    raise TypeError('Invalid param value given for param "%s". %s' % (p.name, e))
            self._paramMap[p] = value
        return self


class HasColumnValidator:

    def _validate(self, column_name, dataset):
        """
        Validate input schema.
        """
        if column_name not in dataset.columns:
            raise ValueError(
                f"Missing input column in transformer {self.uid}: Column '{column_name}' is not present."
            )
        return dataset[column_name]


class HasPartitionMap(Params):

    partitionMap = Param(
        Params._dummy(),
        "partitionMap",
        "Force use pandas udf.",
        typeConverter=TypeConverters.toBoolean,
    )

    def setPartitionMap(self, value):
        """
        Sets the value of :py:attr:`partitionMap`.
        """
        return self._set(partitionMap=value)

    def getPartitionMap(self):
        """
        Sets the value of :py:attr:`partitionMap`.
        """
        return self.getOrDefault(self.partitionMap)


class HasLang(Params):
    lang = Param(Params._dummy(), "lang", "Language.", typeConverter=TypeConverters.toListString)

    def setLang(self, value):
        """
        Sets the value of :py:attr:`lang`.
        """
        return self._set(lang=value)

    def getLang(self) -> str:
        """
        Gets the value of lang or its default value.
        """
        return self.getOrDefault(self.lang)

    def getLangTess(self) -> str:
        """
        Gets the value of lang or its default value.
        """
        return "+".join(
            LANGUAGE_TO_TESSERACT_CODE[CODE_TO_LANGUAGE[lang]]
            for lang in self.getOrDefault(self.lang)
        )


class HasSchema(Params):

    schema = Param(
        Params._dummy(),
        "schema",
        "Output schema.",
        typeConverter=TypeConverters.toString,
    )

    @staticmethod
    def toPydanticSchema(schema):
        schema = json.loads(schema)
        return json_schema_to_model(schema, schema.get("$defs", {}))

    def getPaydanticSchema(self):
        return self.toPydanticSchema(self.getSchema())

    def validateSchema(self, value):
        """
        Validate schema.
        """
        if isinstance(value, str):
            return value
        if issubclass(value, BaseModel):
            value = json.dumps(value.model_json_schema())
        return value

    def getSchema(self):
        """
        Gets the value of schema or its default value.
        """
        return self.getOrDefault(self.schema)

    def setSchema(self, value):
        """
        Sets the value of :py:attr:`schema`.
        """
        return self._set(schema=value)


class HasPrompt(Params):

    prompt = Param(
        Params._dummy(),
        "prompt",
        "Prompt.",
        typeConverter=TypeConverters.toString,
    )
    def getPrompt(self):
        """
        Gets the value of prompt or its default value.
        """
        return self.getOrDefault(self.prompt)

    def setPrompt(self, value):
        """
        Sets the value of :py:attr:`prompt`.
        """
        return self._set(prompt=value)


class HasLLM(Params):
    """
    Mixin for param model.
    """

    model = Param(Params._dummy(), "model", "Model.", typeConverter=TypeConverters.toString)
    apiBase = Param(Params._dummy(), "apiBase", "apiBase.", typeConverter=TypeConverters.toString)
    apiKey = Param(Params._dummy(), "apiKey", "apiKey.", typeConverter=TypeConverters.toString)
    delay = Param(Params._dummy(), "delay", "Delay.", typeConverter=TypeConverters.toInt)
    maxRetry = Param(Params._dummy(), "maxRetry", "Max retry.", typeConverter=TypeConverters.toInt)
    temperature = Param(Params._dummy(), "temperature", "Temperature.", typeConverter=TypeConverters.toFloat)
    systemPrompt = Param(
        Params._dummy(),
        "systemPrompt",
        "System prompt.",
        typeConverter=TypeConverters.toString,
    )

    openAiClient = None
    def __init__(self) -> None:
        super(HasLLM, self).__init__()

    def getOIClient(self):
        from openai import OpenAI
        if self.openAiClient:
            return self.openAiClient
        return self.getClient(self.getApiKey(), self.getApiBase())

    @classmethod
    def getClient(cls, apiKey, apiBase):
        from openai import OpenAI
        kwargs = {}
        if apiKey:
            kwargs["api_key"] = apiKey
        if apiBase:
            kwargs["base_url"] = apiBase
        return OpenAI(**kwargs)

    def getDelay(self):
        """
        Gets the value of delay or its default value.
        """
        return self.getOrDefault(self.delay)

    def getMaxRetry(self):
        """
        Gets the value of maxRetry or its default value.
        """
        return self.getOrDefault(self.maxRetry)

    def getModel(self):
        """
        Gets the value of model or its default value.
        """
        return self.getOrDefault(self.model)

    def setModel(self, value):
        """
        Sets the value of :py:attr:`model`.
        """
        return self._set(model=value)

    def getApiBase(self):
        """
        Gets the value of apiBase or its default value.
        """
        return self.getOrDefault(self.apiBase)

    def setApiBase(self, value):
        """
        Sets the value of :py:attr:`model`.
        """
        return self._set(apiBase=value)

    def getApiKey(self):
        """
        Gets the value of apiKey or its default value.
        """
        return self.getOrDefault(self.apiKey)

    def setApiKey(self, value):
        """
        Sets the value of :py:attr:`apiKey`.
        """
        return self._set(apiKey=value)

    def getSystemPrompt(self):
        """
        Gets the value of systemPrompt or its default value.
        """
        return self.getOrDefault(self.systemPrompt)

    def setSystemPrompt(self, value):
        """
        Sets the value of :py:attr:`systemPrompt`.
        """
        return self._set(systemPrompt=value)

    def getTemperature(self):
        """
        Gets the value of temperature or its default value.
        """
        return self.getOrDefault(self.temperature)


class HasPropagateError(Params):

    propagateError = Param(
        Params._dummy(),
        "propagateError",
        "propagateError.",
        typeConverter=TypeConverters.toBoolean,
    )

    def getPropagateError(self):
        """
        Gets the value of propagateError or its default value.
        """
        return self.getOrDefault(self.propagateError)

    def setPropagateError(self, value):
        """
        Sets the value of :py:attr:`propagateError`.
        """
        return self._set(propagateError=value)