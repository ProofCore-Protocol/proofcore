import { getHttpEndpoint } from "@orbs-network/ton-access";
import { TonClient, WalletContractV4, internal } from "@ton/ton";
import { mnemonicNew, mnemonicToPrivateKey } from "@ton/crypto";
import { ProofRegistry } from "./output/ProofRegistry_ProofRegistry";
import * as fs from "fs";

async function sleep(ms: number) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Обертка авто-повторов при сбоях ноды тестнета
async function safeCall<T>(fn: () => Promise<T>, retries = 5, delayMs = 1500): Promise<T> {
    for (let i = 0; i < retries; i++) {
        try {
            return await fn();
        } catch (e: any) {
            if (i === retries - 1) throw e;
            console.log(`⚠️ Нода тестнета задерживается, повторный запрос (${i + 1}/${retries})...`);
            await sleep(delayMs);
        }
    }
    throw new Error("Не удалось связаться с сетью");
}

async function main() {
    console.log("🌐 Подключаемся к TON Testnet...");
    const endpoint = await getHttpEndpoint({ network: "testnet" });
    const client = new TonClient({ endpoint });

    const mnemonicPath = "./wallet.txt";
    let mnemonics: string[];
    
    if (fs.existsSync(mnemonicPath)) {
        mnemonics = fs.readFileSync(mnemonicPath, "utf-8").trim().split(" ");
        console.log("✅ Загружен кошелек из wallet.txt");
    } else {
        mnemonics = await mnemonicNew();
        fs.writeFileSync(mnemonicPath, mnemonics.join(" "));
        console.log("✨ Сгенерирован НОВЫЙ кошелек!");
    }

    const key = await mnemonicToPrivateKey(mnemonics);
    const wallet = WalletContractV4.create({ publicKey: key.publicKey, workchain: 0 });
    const walletContract = client.open(wallet);

    console.log("💼 Адрес кошелька-деплоера:");
    console.log("   " + wallet.address.toString({ testOnly: true }));

    // Безопасный запрос баланса
    const balance = await safeCall(() => client.getBalance(wallet.address));
    console.log(`💰 Баланс: ${Number(balance) / 1e9} TON`);

    if (balance === 0n) {
        console.log("\n🛑 ОШИБКА: Баланс кошелька равен 0.");
        return;
    }

    const registry = await ProofRegistry.fromInit(wallet.address);
    const contractAddress = registry.address.toString({ testOnly: true });
    console.log("\n🏗 Будущий адрес смарт-контракта ProofRegistry:");
    console.log("   " + contractAddress);

    // Безопасная проверка состояния контракта
    let isAlreadyActive = false;
    try {
        const state = await safeCall(() => client.getContractState(registry.address), 2, 1000);
        if (state.state === "active") {
            isAlreadyActive = true;
        }
    } catch (e) {
        console.log("ℹ️ Контракт еще не создан в сети, переходим к деплою...");
    }

    if (isAlreadyActive) {
        console.log("\n✅ Контракт УЖЕ задеплоен и активен!");
        console.log(`\nСкопируйте в .env:\nTON_MNEMONIC="${mnemonics.join(" ")}"\nCONTRACT_ADDRESS="${contractAddress}"`);
        return;
    }

    console.log("\n🚀 Деплоим контракт в Testnet...");
    const seqno = await safeCall(() => walletContract.getSeqno());

    await walletContract.sendTransfer({
        seqno,
        secretKey: key.secretKey,
        messages: [
            internal({
                to: registry.address,
                value: "0.05",
                init: {
                    code: registry.init!.code,
                    data: registry.init!.data
                }
            })
        ]
    });

    console.log("⏳ Транзакция отправлена в сеть TON. Ждем подтверждения блока...");
    
    let currentSeqno = seqno;
    while (currentSeqno === seqno) {
        await sleep(3000);
        try {
            currentSeqno = await walletContract.getSeqno();
        } catch (e) {
            // Игнорируем промежуточные задержки
        }
    }

    console.log("\n🎉 КОНТРАКТ УСПЕШНО ЗАДЕПЛОЕН В TESTNET!");
    console.log("🔍 Ссылка в Эксплорере: https://testnet.tonviewer.com/" + contractAddress);
    console.log("\n📝 СКОПИРУЙТЕ ЭТИ ДАННЫЕ В ВАШ /opt/proofcore/bot/.env:");
    console.log(`TON_MNEMONIC="${mnemonics.join(" ")}"`);
    console.log(`CONTRACT_ADDRESS="${contractAddress}"`);
}

main().catch(console.error);
