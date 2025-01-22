# Generated from ./visualize/visualize.g4 by ANTLR 4.13.2
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
        4,1,11,68,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,1,0,1,
        0,1,0,1,0,1,0,1,1,3,1,19,8,1,1,1,3,1,22,8,1,1,1,3,1,25,8,1,1,1,3,
        1,28,8,1,3,1,30,8,1,1,2,1,2,1,2,1,2,1,3,1,3,1,3,1,3,1,3,1,4,1,4,
        1,4,1,4,1,4,3,4,46,8,4,1,4,1,4,1,4,5,4,51,8,4,10,4,12,4,54,9,4,1,
        5,1,5,3,5,58,8,5,1,5,1,5,1,5,5,5,63,8,5,10,5,12,5,66,9,5,1,5,0,2,
        8,10,6,0,2,4,6,8,10,0,0,70,0,12,1,0,0,0,2,29,1,0,0,0,4,31,1,0,0,
        0,6,35,1,0,0,0,8,45,1,0,0,0,10,57,1,0,0,0,12,13,5,1,0,0,13,14,3,
        2,1,0,14,15,5,2,0,0,15,16,5,0,0,1,16,1,1,0,0,0,17,19,3,4,2,0,18,
        17,1,0,0,0,18,19,1,0,0,0,19,21,1,0,0,0,20,22,3,6,3,0,21,20,1,0,0,
        0,21,22,1,0,0,0,22,30,1,0,0,0,23,25,3,6,3,0,24,23,1,0,0,0,24,25,
        1,0,0,0,25,27,1,0,0,0,26,28,3,4,2,0,27,26,1,0,0,0,27,28,1,0,0,0,
        28,30,1,0,0,0,29,18,1,0,0,0,29,24,1,0,0,0,30,3,1,0,0,0,31,32,5,6,
        0,0,32,33,5,8,0,0,33,34,5,9,0,0,34,5,1,0,0,0,35,36,5,7,0,0,36,37,
        5,1,0,0,37,38,3,8,4,0,38,39,5,2,0,0,39,7,1,0,0,0,40,46,6,4,-1,0,
        41,42,5,3,0,0,42,43,3,10,5,0,43,44,5,4,0,0,44,46,1,0,0,0,45,40,1,
        0,0,0,45,41,1,0,0,0,46,52,1,0,0,0,47,48,10,1,0,0,48,49,5,5,0,0,49,
        51,3,8,4,2,50,47,1,0,0,0,51,54,1,0,0,0,52,50,1,0,0,0,52,53,1,0,0,
        0,53,9,1,0,0,0,54,52,1,0,0,0,55,58,6,5,-1,0,56,58,5,9,0,0,57,55,
        1,0,0,0,57,56,1,0,0,0,58,64,1,0,0,0,59,60,10,1,0,0,60,61,5,5,0,0,
        61,63,3,10,5,2,62,59,1,0,0,0,63,66,1,0,0,0,64,62,1,0,0,0,64,65,1,
        0,0,0,65,11,1,0,0,0,66,64,1,0,0,0,9,18,21,24,27,29,45,52,57,64
    ]

class visualizeParser ( Parser ):

    grammarFileName = "visualize.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'{'", "'}'", "'('", "')'", "','", "'output'", 
                     "'group'", "'='" ]

    symbolicNames = [ "<INVALID>", "LCURLY", "RCURLY", "LPAREN", "RPAREN", 
                      "COMMA", "OUTPUT", "GROUP", "EQ", "VARIABLE", "ID", 
                      "WS" ]

    RULE_vis_config = 0
    RULE_body = 1
    RULE_output = 2
    RULE_group = 3
    RULE_group_list = 4
    RULE_variable_list = 5

    ruleNames =  [ "vis_config", "body", "output", "group", "group_list", 
                   "variable_list" ]

    EOF = Token.EOF
    LCURLY=1
    RCURLY=2
    LPAREN=3
    RPAREN=4
    COMMA=5
    OUTPUT=6
    GROUP=7
    EQ=8
    VARIABLE=9
    ID=10
    WS=11

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class Vis_configContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LCURLY(self):
            return self.getToken(visualizeParser.LCURLY, 0)

        def body(self):
            return self.getTypedRuleContext(visualizeParser.BodyContext,0)


        def RCURLY(self):
            return self.getToken(visualizeParser.RCURLY, 0)

        def EOF(self):
            return self.getToken(visualizeParser.EOF, 0)

        def getRuleIndex(self):
            return visualizeParser.RULE_vis_config

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVis_config" ):
                return visitor.visitVis_config(self)
            else:
                return visitor.visitChildren(self)




    def vis_config(self):

        localctx = visualizeParser.Vis_configContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_vis_config)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 12
            self.match(visualizeParser.LCURLY)
            self.state = 13
            self.body()
            self.state = 14
            self.match(visualizeParser.RCURLY)
            self.state = 15
            self.match(visualizeParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BodyContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def output(self):
            return self.getTypedRuleContext(visualizeParser.OutputContext,0)


        def group(self):
            return self.getTypedRuleContext(visualizeParser.GroupContext,0)


        def getRuleIndex(self):
            return visualizeParser.RULE_body

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBody" ):
                return visitor.visitBody(self)
            else:
                return visitor.visitChildren(self)




    def body(self):

        localctx = visualizeParser.BodyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_body)
        self._la = 0 # Token type
        try:
            self.state = 29
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,4,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 18
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==6:
                    self.state = 17
                    self.output()


                self.state = 21
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==7:
                    self.state = 20
                    self.group()


                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 24
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==7:
                    self.state = 23
                    self.group()


                self.state = 27
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==6:
                    self.state = 26
                    self.output()


                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OutputContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def OUTPUT(self):
            return self.getToken(visualizeParser.OUTPUT, 0)

        def EQ(self):
            return self.getToken(visualizeParser.EQ, 0)

        def VARIABLE(self):
            return self.getToken(visualizeParser.VARIABLE, 0)

        def getRuleIndex(self):
            return visualizeParser.RULE_output

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOutput" ):
                return visitor.visitOutput(self)
            else:
                return visitor.visitChildren(self)




    def output(self):

        localctx = visualizeParser.OutputContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_output)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 31
            self.match(visualizeParser.OUTPUT)
            self.state = 32
            self.match(visualizeParser.EQ)
            self.state = 33
            self.match(visualizeParser.VARIABLE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class GroupContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def GROUP(self):
            return self.getToken(visualizeParser.GROUP, 0)

        def LCURLY(self):
            return self.getToken(visualizeParser.LCURLY, 0)

        def group_list(self):
            return self.getTypedRuleContext(visualizeParser.Group_listContext,0)


        def RCURLY(self):
            return self.getToken(visualizeParser.RCURLY, 0)

        def getRuleIndex(self):
            return visualizeParser.RULE_group

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitGroup" ):
                return visitor.visitGroup(self)
            else:
                return visitor.visitChildren(self)




    def group(self):

        localctx = visualizeParser.GroupContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_group)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 35
            self.match(visualizeParser.GROUP)
            self.state = 36
            self.match(visualizeParser.LCURLY)
            self.state = 37
            self.group_list(0)
            self.state = 38
            self.match(visualizeParser.RCURLY)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Group_listContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return visualizeParser.RULE_group_list

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class Other_group_listContext(Group_listContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a visualizeParser.Group_listContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def group_list(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(visualizeParser.Group_listContext)
            else:
                return self.getTypedRuleContext(visualizeParser.Group_listContext,i)

        def COMMA(self):
            return self.getToken(visualizeParser.COMMA, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOther_group_list" ):
                return visitor.visitOther_group_list(self)
            else:
                return visitor.visitChildren(self)


    class Base_groupContext(Group_listContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a visualizeParser.Group_listContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LPAREN(self):
            return self.getToken(visualizeParser.LPAREN, 0)
        def variable_list(self):
            return self.getTypedRuleContext(visualizeParser.Variable_listContext,0)

        def RPAREN(self):
            return self.getToken(visualizeParser.RPAREN, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBase_group" ):
                return visitor.visitBase_group(self)
            else:
                return visitor.visitChildren(self)


    class Empty_groupContext(Group_listContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a visualizeParser.Group_listContext
            super().__init__(parser)
            self.copyFrom(ctx)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEmpty_group" ):
                return visitor.visitEmpty_group(self)
            else:
                return visitor.visitChildren(self)



    def group_list(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = visualizeParser.Group_listContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 8
        self.enterRecursionRule(localctx, 8, self.RULE_group_list, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 45
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,5,self._ctx)
            if la_ == 1:
                localctx = visualizeParser.Empty_groupContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                pass

            elif la_ == 2:
                localctx = visualizeParser.Base_groupContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 41
                self.match(visualizeParser.LPAREN)
                self.state = 42
                self.variable_list(0)
                self.state = 43
                self.match(visualizeParser.RPAREN)
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 52
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,6,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = visualizeParser.Other_group_listContext(self, visualizeParser.Group_listContext(self, _parentctx, _parentState))
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_group_list)
                    self.state = 47
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 48
                    self.match(visualizeParser.COMMA)
                    self.state = 49
                    self.group_list(2) 
                self.state = 54
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,6,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class Variable_listContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return visualizeParser.RULE_variable_list

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class Other_var_listContext(Variable_listContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a visualizeParser.Variable_listContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def variable_list(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(visualizeParser.Variable_listContext)
            else:
                return self.getTypedRuleContext(visualizeParser.Variable_listContext,i)

        def COMMA(self):
            return self.getToken(visualizeParser.COMMA, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOther_var_list" ):
                return visitor.visitOther_var_list(self)
            else:
                return visitor.visitChildren(self)


    class Empty_var_listContext(Variable_listContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a visualizeParser.Variable_listContext
            super().__init__(parser)
            self.copyFrom(ctx)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEmpty_var_list" ):
                return visitor.visitEmpty_var_list(self)
            else:
                return visitor.visitChildren(self)


    class Base_var_listContext(Variable_listContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a visualizeParser.Variable_listContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def VARIABLE(self):
            return self.getToken(visualizeParser.VARIABLE, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBase_var_list" ):
                return visitor.visitBase_var_list(self)
            else:
                return visitor.visitChildren(self)



    def variable_list(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = visualizeParser.Variable_listContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 10
        self.enterRecursionRule(localctx, 10, self.RULE_variable_list, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 57
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,7,self._ctx)
            if la_ == 1:
                localctx = visualizeParser.Empty_var_listContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                pass

            elif la_ == 2:
                localctx = visualizeParser.Base_var_listContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 56
                self.match(visualizeParser.VARIABLE)
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 64
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,8,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = visualizeParser.Other_var_listContext(self, visualizeParser.Variable_listContext(self, _parentctx, _parentState))
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_variable_list)
                    self.state = 59
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 60
                    self.match(visualizeParser.COMMA)
                    self.state = 61
                    self.variable_list(2) 
                self.state = 66
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,8,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[4] = self.group_list_sempred
        self._predicates[5] = self.variable_list_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def group_list_sempred(self, localctx:Group_listContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 1)
         

    def variable_list_sempred(self, localctx:Variable_listContext, predIndex:int):
            if predIndex == 1:
                return self.precpred(self._ctx, 1)
         




