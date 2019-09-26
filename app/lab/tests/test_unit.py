import unittest
import sys
import os
import argparse
import shutil


class DjangoRestCLIUnitTest(unittest.TestCase):
    def setUp(self):
        try:
            from djangorestcli.controllers.DjangoRestCLIController import DjangoRestCLIController
            self.controller = DjangoRestCLIController()
        except:
            self.fail('module not found')

    @classmethod
    def setUpClass(cls):
        cls.currentDirectory = os.getcwd()
        cls.moduleDirectory = os.path.dirname(os.path.abspath(__file__))
        cls.parser = argparse.ArgumentParser(
            description='Generate django rest models views and serializers automaticaly')
        cls.parser.add_argument('--make', type=str, nargs='+',
                                help='?')
        sys.path.append(os.path.abspath(
            os.path.join(cls.moduleDirectory, '..')))

        cls.appName = "api"

        os.mkdir(os.path.join(cls.currentDirectory, cls.appName))
        os.mkdir(os.path.join(cls.currentDirectory,
                              os.path.basename(cls.currentDirectory)))
        with open(os.path.join(cls.currentDirectory, 'manage.py'), 'w') as file:
            file.close()

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(os.path.join(cls.currentDirectory, cls.appName))
        shutil.rmtree(os.path.join(cls.currentDirectory,
                                   os.path.basename(cls.currentDirectory)))
        os.remove(os.path.join(cls.currentDirectory, 'manage.py'))

    def test_controller(self):
        self.assertEqual(self.controller.currentDirectory,
                         self.currentDirectory)
        with open(os.path.join(self.moduleDirectory, '..', 'djangorestcli', 'templates', 'modeltemplate.txt'), 'r') as file:
            self.assertEqual(self.controller.modelTemplate, file.read())
            file.close()
        with open(os.path.join(self.moduleDirectory, '..', 'djangorestcli', 'templates', 'viewtemplate.txt'), 'r') as file:
            self.assertEqual(self.controller.viewTemplate, file.read())
            file.close()
        with open(os.path.join(self.moduleDirectory, '..', 'djangorestcli', 'templates', 'serializertemplate.txt'), 'r') as file:
            self.assertEqual(self.controller.serializerTemplate, file.read())
            file.close()

    def test_argparse(self):
        argv = ['--make', 'rest.description']
        args = self.parser.parse_args(argv)
        self.assertIsNotNone(args.make)
        self.assertEqual(args.make, [argv[1]])

        with self.assertRaises(SystemExit):
            argv = ['--make']
            args = self.parser.parse_args(argv)
        with self.assertRaises(SystemExit):
            argv = ['--generic']
            args = self.parser.parse_args(argv)

    def test_controller_run(self):
        argv = ['--make', self.appName+'.user']
        appName, modelName = argv[1].split('.')
        modelName = modelName.capitalize()
        args = self.parser.parse_args(argv)
        self.controller.generate(args)
        self.assertEqual(self.controller.isADjangoDirectory(), True)
        self.assertEqual(True, os.path.exists(
            os.path.join(self.currentDirectory, appName, 'models')))
        self.assertEqual(True, os.path.exists(
            os.path.join(self.currentDirectory, appName, 'views')))
        self.assertEqual(True, os.path.exists(
            os.path.join(self.currentDirectory, appName, 'serializers')))

        self.assertEqual(True, os.path.exists(
            os.path.join(self.currentDirectory, appName, 'models', modelName+"Model.py")))
        self.assertEqual(True, os.path.exists(
            os.path.join(self.currentDirectory, appName, 'views', modelName+"View.py")))
        self.assertEqual(True, os.path.exists(
            os.path.join(self.currentDirectory, appName, 'serializers', modelName+"Serializer.py")))

        argv = ['--make', self.appName+'.description']
        appName, modelName = argv[1].split('.')
        modelName = modelName.capitalize()
        args = self.parser.parse_args(argv)
        self.controller.generate(args)
        self.assertEqual(self.controller.isADjangoDirectory(), True)
        self.assertEqual(True, os.path.exists(
            os.path.join(self.currentDirectory, appName, 'models')))
        self.assertEqual(True, os.path.exists(
            os.path.join(self.currentDirectory, appName, 'views')))
        self.assertEqual(True, os.path.exists(
            os.path.join(self.currentDirectory, appName, 'serializers')))

        self.assertEqual(True, os.path.exists(
            os.path.join(self.currentDirectory, appName, 'models', modelName+"Model.py")))
        self.assertEqual(True, os.path.exists(
            os.path.join(self.currentDirectory, appName, 'views', modelName+"View.py")))
        self.assertEqual(True, os.path.exists(
            os.path.join(self.currentDirectory, appName, 'serializers', modelName+"Serializer.py")))
