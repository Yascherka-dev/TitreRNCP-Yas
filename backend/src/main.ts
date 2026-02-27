import { NestFactory } from '@nestjs/core';
import { ValidationPipe } from '@nestjs/common';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';
import { AppModule } from './app.module';
import { HttpExceptionFilter } from './common/filters/http-exception.filter';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // CORS — autorise le frontend Angular
  app.enableCors({
    origin: process.env.FRONTEND_URL ?? 'http://localhost:4200',
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization'],
  });

  // Validation globale des DTOs (class-validator)
  app.useGlobalPipes(
    new ValidationPipe({
      whitelist: true,        // Ignore les champs non déclarés dans le DTO
      forbidNonWhitelisted: true,
      transform: true,        // Caste automatiquement les types (string → number, etc.)
    }),
  );

  // Filtre global pour formater proprement les erreurs HTTP
  app.useGlobalFilters(new HttpExceptionFilter());

  // Swagger — accessible sur /api
  const config = new DocumentBuilder()
    .setTitle('Match & Munch API')
    .setDescription('API backend — matchs, suggestions de recettes, auth, favoris')
    .setVersion('1.0')
    .addBearerAuth()
    .build();
  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('api', app, document);

  const port = process.env.PORT ?? 3000;
  await app.listen(port);
  console.log(`🍽️  Match & Munch API démarrée sur http://localhost:${port}`);
  console.log(`📚  Swagger : http://localhost:${port}/api`);
}
bootstrap();
