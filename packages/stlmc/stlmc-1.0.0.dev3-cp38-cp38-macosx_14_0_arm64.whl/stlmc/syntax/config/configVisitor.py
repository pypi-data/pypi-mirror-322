# Generated from ./config/config.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .configParser import configParser
else:
    from configParser import configParser

# This class defines a complete generic visitor for a parse tree produced by configParser.

class configVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by configParser#config.
    def visitConfig(self, ctx:configParser.ConfigContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by configParser#basic_section.
    def visitBasic_section(self, ctx:configParser.Basic_sectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by configParser#extend_section.
    def visitExtend_section(self, ctx:configParser.Extend_sectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by configParser#list_of_name.
    def visitList_of_name(self, ctx:configParser.List_of_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by configParser#single_names.
    def visitSingle_names(self, ctx:configParser.Single_namesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by configParser#args.
    def visitArgs(self, ctx:configParser.ArgsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by configParser#arg_assn.
    def visitArg_assn(self, ctx:configParser.Arg_assnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by configParser#arg.
    def visitArg(self, ctx:configParser.ArgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by configParser#string_val.
    def visitString_val(self, ctx:configParser.String_valContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by configParser#multi_string_val.
    def visitMulti_string_val(self, ctx:configParser.Multi_string_valContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by configParser#runall_val.
    def visitRunall_val(self, ctx:configParser.Runall_valContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by configParser#runlabeled_only.
    def visitRunlabeled_only(self, ctx:configParser.Runlabeled_onlyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by configParser#number_val.
    def visitNumber_val(self, ctx:configParser.Number_valContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by configParser#empty_val.
    def visitEmpty_val(self, ctx:configParser.Empty_valContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by configParser#list_of_variable_names.
    def visitList_of_variable_names(self, ctx:configParser.List_of_variable_namesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by configParser#single_variable_name.
    def visitSingle_variable_name(self, ctx:configParser.Single_variable_nameContext):
        return self.visitChildren(ctx)



del configParser