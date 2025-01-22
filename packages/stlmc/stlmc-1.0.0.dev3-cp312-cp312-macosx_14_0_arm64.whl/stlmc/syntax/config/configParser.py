# Generated from ./config/config.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,14,76,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,1,0,5,0,18,8,0,10,0,12,0,21,9,0,1,0,1,0,1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,1,37,8,1,1,2,1,2,1,2,1,2,3,2,
        43,8,2,1,3,5,3,46,8,3,10,3,12,3,49,9,3,1,4,1,4,1,4,1,4,1,5,1,5,1,
        6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,3,6,68,8,6,1,7,1,7,1,7,
        1,7,3,7,74,8,7,1,7,0,0,8,0,2,4,6,8,10,12,14,0,0,77,0,19,1,0,0,0,
        2,36,1,0,0,0,4,42,1,0,0,0,6,47,1,0,0,0,8,50,1,0,0,0,10,54,1,0,0,
        0,12,67,1,0,0,0,14,73,1,0,0,0,16,18,3,2,1,0,17,16,1,0,0,0,18,21,
        1,0,0,0,19,17,1,0,0,0,19,20,1,0,0,0,20,22,1,0,0,0,21,19,1,0,0,0,
        22,23,5,0,0,1,23,1,1,0,0,0,24,25,5,13,0,0,25,26,5,5,0,0,26,27,3,
        6,3,0,27,28,5,6,0,0,28,37,1,0,0,0,29,30,5,13,0,0,30,31,5,4,0,0,31,
        32,3,4,2,0,32,33,5,5,0,0,33,34,3,6,3,0,34,35,5,6,0,0,35,37,1,0,0,
        0,36,24,1,0,0,0,36,29,1,0,0,0,37,3,1,0,0,0,38,39,5,13,0,0,39,40,
        5,9,0,0,40,43,3,4,2,0,41,43,5,13,0,0,42,38,1,0,0,0,42,41,1,0,0,0,
        43,5,1,0,0,0,44,46,3,8,4,0,45,44,1,0,0,0,46,49,1,0,0,0,47,45,1,0,
        0,0,47,48,1,0,0,0,48,7,1,0,0,0,49,47,1,0,0,0,50,51,3,10,5,0,51,52,
        5,11,0,0,52,53,3,12,6,0,53,9,1,0,0,0,54,55,5,13,0,0,55,11,1,0,0,
        0,56,57,5,10,0,0,57,58,5,13,0,0,58,68,5,10,0,0,59,60,5,10,0,0,60,
        61,3,14,7,0,61,62,5,10,0,0,62,68,1,0,0,0,63,68,5,1,0,0,64,68,5,2,
        0,0,65,68,5,12,0,0,66,68,1,0,0,0,67,56,1,0,0,0,67,59,1,0,0,0,67,
        63,1,0,0,0,67,64,1,0,0,0,67,65,1,0,0,0,67,66,1,0,0,0,68,13,1,0,0,
        0,69,70,5,13,0,0,70,71,5,9,0,0,71,74,3,14,7,0,72,74,5,13,0,0,73,
        69,1,0,0,0,73,72,1,0,0,0,74,15,1,0,0,0,6,19,36,42,47,67,73
    ]

class configParser ( Parser ):

    grammarFileName = "config.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'run-all'", "'run-labeled-only'", "'mandatory'", 
                     "'extends'", "'{'", "'}'", "'('", "')'", "','", "'\"'", 
                     "'='" ]

    symbolicNames = [ "<INVALID>", "RUNALL", "RUNLABELED", "MANDATORY", 
                      "EXTENDS", "LCURLY", "RCURLY", "LTUPLE", "RTUPLE", 
                      "COMMA", "QUOTE", "EQ", "NUMBER", "VALUE", "WS" ]

    RULE_config = 0
    RULE_section = 1
    RULE_names = 2
    RULE_args = 3
    RULE_arg_assn = 4
    RULE_arg = 5
    RULE_value = 6
    RULE_varible_names = 7

    ruleNames =  [ "config", "section", "names", "args", "arg_assn", "arg", 
                   "value", "varible_names" ]

    EOF = Token.EOF
    RUNALL=1
    RUNLABELED=2
    MANDATORY=3
    EXTENDS=4
    LCURLY=5
    RCURLY=6
    LTUPLE=7
    RTUPLE=8
    COMMA=9
    QUOTE=10
    EQ=11
    NUMBER=12
    VALUE=13
    WS=14

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ConfigContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(configParser.EOF, 0)

        def section(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(configParser.SectionContext)
            else:
                return self.getTypedRuleContext(configParser.SectionContext,i)


        def getRuleIndex(self):
            return configParser.RULE_config

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitConfig" ):
                return visitor.visitConfig(self)
            else:
                return visitor.visitChildren(self)




    def config(self):

        localctx = configParser.ConfigContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_config)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 19
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==13:
                self.state = 16
                self.section()
                self.state = 21
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 22
            self.match(configParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SectionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return configParser.RULE_section

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class Basic_sectionContext(SectionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a configParser.SectionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def VALUE(self):
            return self.getToken(configParser.VALUE, 0)
        def LCURLY(self):
            return self.getToken(configParser.LCURLY, 0)
        def args(self):
            return self.getTypedRuleContext(configParser.ArgsContext,0)

        def RCURLY(self):
            return self.getToken(configParser.RCURLY, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBasic_section" ):
                return visitor.visitBasic_section(self)
            else:
                return visitor.visitChildren(self)


    class Extend_sectionContext(SectionContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a configParser.SectionContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def VALUE(self):
            return self.getToken(configParser.VALUE, 0)
        def EXTENDS(self):
            return self.getToken(configParser.EXTENDS, 0)
        def names(self):
            return self.getTypedRuleContext(configParser.NamesContext,0)

        def LCURLY(self):
            return self.getToken(configParser.LCURLY, 0)
        def args(self):
            return self.getTypedRuleContext(configParser.ArgsContext,0)

        def RCURLY(self):
            return self.getToken(configParser.RCURLY, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExtend_section" ):
                return visitor.visitExtend_section(self)
            else:
                return visitor.visitChildren(self)



    def section(self):

        localctx = configParser.SectionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_section)
        try:
            self.state = 36
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                localctx = configParser.Basic_sectionContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 24
                self.match(configParser.VALUE)
                self.state = 25
                self.match(configParser.LCURLY)
                self.state = 26
                self.args()
                self.state = 27
                self.match(configParser.RCURLY)
                pass

            elif la_ == 2:
                localctx = configParser.Extend_sectionContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 29
                self.match(configParser.VALUE)
                self.state = 30
                self.match(configParser.EXTENDS)
                self.state = 31
                self.names()
                self.state = 32
                self.match(configParser.LCURLY)
                self.state = 33
                self.args()
                self.state = 34
                self.match(configParser.RCURLY)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NamesContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return configParser.RULE_names

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class List_of_nameContext(NamesContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a configParser.NamesContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def VALUE(self):
            return self.getToken(configParser.VALUE, 0)
        def COMMA(self):
            return self.getToken(configParser.COMMA, 0)
        def names(self):
            return self.getTypedRuleContext(configParser.NamesContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitList_of_name" ):
                return visitor.visitList_of_name(self)
            else:
                return visitor.visitChildren(self)


    class Single_namesContext(NamesContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a configParser.NamesContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def VALUE(self):
            return self.getToken(configParser.VALUE, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSingle_names" ):
                return visitor.visitSingle_names(self)
            else:
                return visitor.visitChildren(self)



    def names(self):

        localctx = configParser.NamesContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_names)
        try:
            self.state = 42
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
            if la_ == 1:
                localctx = configParser.List_of_nameContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 38
                self.match(configParser.VALUE)
                self.state = 39
                self.match(configParser.COMMA)
                self.state = 40
                self.names()
                pass

            elif la_ == 2:
                localctx = configParser.Single_namesContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 41
                self.match(configParser.VALUE)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArgsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def arg_assn(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(configParser.Arg_assnContext)
            else:
                return self.getTypedRuleContext(configParser.Arg_assnContext,i)


        def getRuleIndex(self):
            return configParser.RULE_args

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArgs" ):
                return visitor.visitArgs(self)
            else:
                return visitor.visitChildren(self)




    def args(self):

        localctx = configParser.ArgsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_args)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 47
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==13:
                self.state = 44
                self.arg_assn()
                self.state = 49
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Arg_assnContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def arg(self):
            return self.getTypedRuleContext(configParser.ArgContext,0)


        def EQ(self):
            return self.getToken(configParser.EQ, 0)

        def value(self):
            return self.getTypedRuleContext(configParser.ValueContext,0)


        def getRuleIndex(self):
            return configParser.RULE_arg_assn

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArg_assn" ):
                return visitor.visitArg_assn(self)
            else:
                return visitor.visitChildren(self)




    def arg_assn(self):

        localctx = configParser.Arg_assnContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_arg_assn)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 50
            self.arg()
            self.state = 51
            self.match(configParser.EQ)
            self.state = 52
            self.value()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArgContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def VALUE(self):
            return self.getToken(configParser.VALUE, 0)

        def getRuleIndex(self):
            return configParser.RULE_arg

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArg" ):
                return visitor.visitArg(self)
            else:
                return visitor.visitChildren(self)




    def arg(self):

        localctx = configParser.ArgContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_arg)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 54
            self.match(configParser.VALUE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return configParser.RULE_value

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class String_valContext(ValueContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a configParser.ValueContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def QUOTE(self, i:int=None):
            if i is None:
                return self.getTokens(configParser.QUOTE)
            else:
                return self.getToken(configParser.QUOTE, i)
        def VALUE(self):
            return self.getToken(configParser.VALUE, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitString_val" ):
                return visitor.visitString_val(self)
            else:
                return visitor.visitChildren(self)


    class Multi_string_valContext(ValueContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a configParser.ValueContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def QUOTE(self, i:int=None):
            if i is None:
                return self.getTokens(configParser.QUOTE)
            else:
                return self.getToken(configParser.QUOTE, i)
        def varible_names(self):
            return self.getTypedRuleContext(configParser.Varible_namesContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMulti_string_val" ):
                return visitor.visitMulti_string_val(self)
            else:
                return visitor.visitChildren(self)


    class Runall_valContext(ValueContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a configParser.ValueContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def RUNALL(self):
            return self.getToken(configParser.RUNALL, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRunall_val" ):
                return visitor.visitRunall_val(self)
            else:
                return visitor.visitChildren(self)


    class Empty_valContext(ValueContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a configParser.ValueContext
            super().__init__(parser)
            self.copyFrom(ctx)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEmpty_val" ):
                return visitor.visitEmpty_val(self)
            else:
                return visitor.visitChildren(self)


    class Runlabeled_onlyContext(ValueContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a configParser.ValueContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def RUNLABELED(self):
            return self.getToken(configParser.RUNLABELED, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRunlabeled_only" ):
                return visitor.visitRunlabeled_only(self)
            else:
                return visitor.visitChildren(self)


    class Number_valContext(ValueContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a configParser.ValueContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def NUMBER(self):
            return self.getToken(configParser.NUMBER, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNumber_val" ):
                return visitor.visitNumber_val(self)
            else:
                return visitor.visitChildren(self)



    def value(self):

        localctx = configParser.ValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_value)
        try:
            self.state = 67
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,4,self._ctx)
            if la_ == 1:
                localctx = configParser.String_valContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 56
                self.match(configParser.QUOTE)
                self.state = 57
                self.match(configParser.VALUE)
                self.state = 58
                self.match(configParser.QUOTE)
                pass

            elif la_ == 2:
                localctx = configParser.Multi_string_valContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 59
                self.match(configParser.QUOTE)
                self.state = 60
                self.varible_names()
                self.state = 61
                self.match(configParser.QUOTE)
                pass

            elif la_ == 3:
                localctx = configParser.Runall_valContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 63
                self.match(configParser.RUNALL)
                pass

            elif la_ == 4:
                localctx = configParser.Runlabeled_onlyContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 64
                self.match(configParser.RUNLABELED)
                pass

            elif la_ == 5:
                localctx = configParser.Number_valContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 65
                self.match(configParser.NUMBER)
                pass

            elif la_ == 6:
                localctx = configParser.Empty_valContext(self, localctx)
                self.enterOuterAlt(localctx, 6)

                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Varible_namesContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return configParser.RULE_varible_names

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class List_of_variable_namesContext(Varible_namesContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a configParser.Varible_namesContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def VALUE(self):
            return self.getToken(configParser.VALUE, 0)
        def COMMA(self):
            return self.getToken(configParser.COMMA, 0)
        def varible_names(self):
            return self.getTypedRuleContext(configParser.Varible_namesContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitList_of_variable_names" ):
                return visitor.visitList_of_variable_names(self)
            else:
                return visitor.visitChildren(self)


    class Single_variable_nameContext(Varible_namesContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a configParser.Varible_namesContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def VALUE(self):
            return self.getToken(configParser.VALUE, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSingle_variable_name" ):
                return visitor.visitSingle_variable_name(self)
            else:
                return visitor.visitChildren(self)



    def varible_names(self):

        localctx = configParser.Varible_namesContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_varible_names)
        try:
            self.state = 73
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,5,self._ctx)
            if la_ == 1:
                localctx = configParser.List_of_variable_namesContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 69
                self.match(configParser.VALUE)
                self.state = 70
                self.match(configParser.COMMA)
                self.state = 71
                self.varible_names()
                pass

            elif la_ == 2:
                localctx = configParser.Single_variable_nameContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 72
                self.match(configParser.VALUE)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





