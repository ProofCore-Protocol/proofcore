import "@stdlib/deploy";
import "@stdlib/ownable";

message(0x12345678) AnchorBatch {
    batch_id: String;
    merkle_root: String;
}

message BatchAnchoredEvent {
    batch_id: String;
    merkle_root: String;
    timestamp: Int as uint32;
    sender: Address;
}

contract ProofRegistry with Deployable, Ownable {

    owner: Address;
    total_batches: Int as uint32;

    init(owner: Address) {
        self.owner = owner;
        self.total_batches = 0;
    }

    receive(msg: AnchorBatch) {
        self.requireOwner();
        self.total_batches = self.total_batches + 1;

        emit(BatchAnchoredEvent{
            batch_id: msg.batch_id,
            merkle_root: msg.merkle_root,
            timestamp: now(),
            sender: sender()
        }.toCell());

        // 🚨 ВЫВОДИМ MERKLE ROOT ПРЯМО В ТЕКСТОВЫЙ КОММЕНТАРИЙ ТРАНЗАКЦИИ!
        let comment: StringBuilder = beginComment();
        comment.append("Merkle Root: ");
        comment.append(msg.merkle_root);

        self.reply(comment.toCell());
    }

    get fun getTotalBatches(): Int {
        return self.total_batches;
    }
}
