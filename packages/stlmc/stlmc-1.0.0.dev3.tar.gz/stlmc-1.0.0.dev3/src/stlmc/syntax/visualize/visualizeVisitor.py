# Generated from ./visualize/visualize.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .visualizeParser import visualizeParser
else:
    from visualizeParser import visualizeParser

# This class defines a complete generic visitor for a parse tree produced by visualizeParser.

class visualizeVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by visualizeParser#vis_config.
    def visitVis_config(self, ctx:visualizeParser.Vis_configContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by visualizeParser#body.
    def visitBody(self, ctx:visualizeParser.BodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by visualizeParser#output.
    def visitOutput(self, ctx:visualizeParser.OutputContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by visualizeParser#group.
    def visitGroup(self, ctx:visualizeParser.GroupContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by visualizeParser#other_group_list.
    def visitOther_group_list(self, ctx:visualizeParser.Other_group_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by visualizeParser#base_group.
    def visitBase_group(self, ctx:visualizeParser.Base_groupContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by visualizeParser#empty_group.
    def visitEmpty_group(self, ctx:visualizeParser.Empty_groupContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by visualizeParser#other_var_list.
    def visitOther_var_list(self, ctx:visualizeParser.Other_var_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by visualizeParser#empty_var_list.
    def visitEmpty_var_list(self, ctx:visualizeParser.Empty_var_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by visualizeParser#base_var_list.
    def visitBase_var_list(self, ctx:visualizeParser.Base_var_listContext):
        return self.visitChildren(ctx)



del visualizeParser