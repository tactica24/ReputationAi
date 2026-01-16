import { PrismaClient } from '@prisma/client';
import bcrypt from 'bcryptjs';

const prisma = new PrismaClient();

async function main() {
  const sources = [
    {
      type: 'RSS',
      url: 'https://example.com/rss/policy',
      enabled: true,
      sectionHint: 'Policy'
    },
    {
      type: 'RSS',
      url: 'https://example.com/rss/finance',
      enabled: true,
      sectionHint: 'Finance'
    },
    {
      type: 'WEBPAGE',
      url: 'https://example.com/infra',
      enabled: true,
      sectionHint: 'Infrastructure'
    }
  ];

  await Promise.all(
    sources.map((source) =>
      prisma.source.upsert({
        where: { url: source.url },
        update: source,
        create: source
      })
    )
  );

  const adminEmail = process.env.ADMIN_EMAIL;
  const adminPassword = process.env.ADMIN_PASSWORD;

  if (adminEmail && adminPassword) {
    const passwordHash = await bcrypt.hash(adminPassword, 10);
    await prisma.admin.upsert({
      where: { email: adminEmail },
      update: { passwordHash },
      create: { email: adminEmail, passwordHash }
    });
  } else {
    console.warn('ADMIN_EMAIL or ADMIN_PASSWORD not set; skipping admin seed.');
  }
}

main()
  .catch((error) => {
    console.error(error);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
