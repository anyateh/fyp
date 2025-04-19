class Queue {
    constructor(capacity) {
        this.items = [];
        this.limit = capacity;
        this.enqueue_ptr = 0;
        this.dequeue_ptr = 0;
    }

    cyclic_inc(n) {
        if (n < this.limit - 1) {
            return n + 1;
        }

        return 0;
    }

    enqueue(item) {
        // if (this.items.length < this.limit) {
        //     this.items.push(item);
        //     this.enqueue_ptr = this.cyclic_inc(this.enqueue_ptr);
        //     return;
        // }

        this.items[this.enqueue_ptr] = item;
        this.enqueue_ptr = this.cyclic_inc(this.enqueue_ptr);
        if (this.enqueue_ptr == this.dequeue_ptr) {
            this.dequeue_ptr = this.cyclic_inc(this.dequeue_ptr);
        }
    }

    peek() {
        return this.items[this.dequeue_ptr];
    }

    dequeue() {
        var item = this.items[this.dequeue_ptr];
        this.dequeue_ptr = this.cyclic_inc(this.dequeue_ptr);
        return item;
    }

    clear() {
        this.items.length = 0;
        this.dequeue_ptr = 0;
        this.enqueue_ptr = 0;
    }

    is_empty() {
        return this.items.length == 0;
    }
}